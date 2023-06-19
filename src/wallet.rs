use stacks_rs::address::StacksAddress;
use stacks_rs::crypto::c32_address;
use stacks_rs::crypto::ExtendedPrivateKey;
use pyo3::prelude::*;
use std::collections::HashMap;
use bip39;
use pyo3::exceptions::PyValueError;
use pyo3::exceptions::PyException;
use secp256k1::PublicKey;
use secp256k1::SecretKey;
use pyo3::types::PyBytes;
use pyo3::exceptions;

#[pyclass]
#[derive(Debug, Copy, Clone, PartialEq, Eq, PartialOrd, Ord)]
pub enum AddressVersion {
    MainnetP2PKH = 22,
    MainnetP2SH = 20,
    TestnetP2PKH = 26,
    TestnetP2SH = 21,
}

#[pyclass]
#[derive(Clone)]
pub struct PyPublicKey {
    pub_key: PublicKey,
}

#[pymethods]
impl PyPublicKey {
    #[new]
    pub fn new(data: &[u8]) -> PyResult<Self> {
        let public_key = match PublicKey::from_slice(data) {
            Ok(x) => Ok(PyPublicKey { pub_key: x }),
            Err(error) => Err(exceptions::PyValueError::new_err(format!("{}", error))),
        };
        public_key
    }

    fn serialize(&self, py: Python, compressed: bool) -> Py<PyBytes> {
        if compressed {
            PyBytes::new(py, &self.pub_key.serialize()).into()
        } else {
            PyBytes::new(py, &self.pub_key.serialize_uncompressed()).into()
        }
    }

    fn to_string(&self) -> String {
        format!("{:?}", self.pub_key)
    }
}

impl From<PyPublicKey> for PublicKey {
    fn from(py_key: PyPublicKey) -> Self {
        py_key.pub_key
    }
}

#[pyclass]
#[derive(Clone)]
pub struct PyPrivateKey {
    sec_key: SecretKey,
}

impl PyPrivateKey {
    pub fn get_inner_sec_key(&self) -> SecretKey {
        self.sec_key
    }
}

#[pymethods]
impl PyPrivateKey {
    #[new]
    fn new(data: &[u8]) -> PyResult<Self> {
        let secret_key = match SecretKey::from_slice(&data) {
            Ok(x) => Ok(PyPrivateKey { sec_key: x }),
            Err(error) => Err(exceptions::PyValueError::new_err(format!("{}", error))),
        };
        secret_key
    }

    pub fn serialize(&self, py: Python) -> Py<PyBytes> {
        PyBytes::new(py, &self.sec_key[..]).into()
    }
}

pub type StacksPublicKey = PyPublicKey;
pub type StacksPrivateKey = PyPrivateKey;

const STX_DERIVATION_PATH: &str = "m/44'/5757'/0'/0";

#[pyclass]
#[derive(Clone)]
struct PyExtendedPrivateKey {
    ext_priv_key: ExtendedPrivateKey,
}

#[pymethods]
impl PyExtendedPrivateKey {
    #[new]
    fn new(data: &[u8]) -> PyResult<Self> {
        let ext_priv_key = ExtendedPrivateKey::from_seed(data).map_err(|err| {
            PyErr::new::<exceptions::PyValueError, _>(format!("Failed to create extended private key: {}", err))
        })?;
        Ok(PyExtendedPrivateKey { ext_priv_key })
    }
}

impl From<PyExtendedPrivateKey> for ExtendedPrivateKey {
    fn from(py_ext_priv_key: PyExtendedPrivateKey) -> Self {
        py_ext_priv_key.ext_priv_key
    }
}

#[pyclass]
#[derive(Clone)]
struct StacksAccount {
    pub index: u32,
    pub public_key: StacksPublicKey,
    pub private_key: StacksPrivateKey
}

#[pymethods]
impl StacksAccount {
    #[new]
    fn new(index: u32, public_key: StacksPublicKey, private_key: StacksPrivateKey) -> Self {
        Self {
           index,
           public_key,
           private_key 
        }
    }
    #[getter]
    fn index(&self) -> u32 {
        self.index.clone()
    }

    #[getter]
    fn public_key(&self) -> StacksPublicKey {
        self.public_key.clone()
    }

    #[getter]
    fn private_key(&self) -> StacksPrivateKey {
        self.private_key.clone()
    }

    fn get_address(&self, version: AddressVersion) -> PyResult<String> {
        let address = StacksAddress::from_public_key(self.public_key.pub_key.clone(), None)
            .map_err(|err| PyErr::new::<PyValueError, _>(format!("Failed to create address: {}", err)))?;
        let c32 = c32_address(address.as_bytes(), version as u8)
            .map_err(|err| PyErr::new::<PyValueError, _>(format!("Failed to convert address to c32 format: {}", err)))?;
        Ok(c32)
    }
}

fn derive(root: &PyExtendedPrivateKey, index: u32) -> PyResult<StacksAccount> {
    let child = root.ext_priv_key.derive(STX_DERIVATION_PATH).map_err(|err| {
        PyErr::new::<exceptions::PyValueError, _>(format!("Failed to derive child key: {}", err))
    })?.child(index.into()).map_err(|err| {
        PyErr::new::<exceptions::PyValueError, _>(format!("Failed to derive child key with index {}: {}", index, err))
    })?;
    let public_key = child.public_key();
    let private_key = child.private_key;
    Ok(StacksAccount::new(
        index,
        PyPublicKey { pub_key: public_key },
        PyPrivateKey { sec_key: private_key },
    ))
}

#[pyclass]
struct StacksWallet {
    root_key: PyExtendedPrivateKey,
    accounts: HashMap<u32, StacksAccount>,
}

#[pymethods]
impl StacksWallet {
    #[new]
    fn new(secret_key: String) -> PyResult<Self> {
        let mnemonic = bip39::Mnemonic::parse(&secret_key).map_err(|err| {
            PyErr::new::<PyException, _>(format!("Failed to generate mnemonic: {}", err))
        })?;
        let seed = mnemonic.to_seed_normalized("");
        let root_key = PyExtendedPrivateKey::new(&seed)?;
        Ok(StacksWallet {
            root_key,
            accounts: HashMap::new(),
        })
    }

    fn get_account(&mut self, index: u32) -> PyResult<StacksAccount> {
        if let Some(account) = self.accounts.get(&index) {
            Ok(account.clone())
        } else {
            let account = derive(&self.root_key, index).map_err(|err| {
                PyErr::new::<PyException, _>(format!("Failed to drive stacksaccount from root key: {}", err))
            })?;
            self.set_account(index, account.clone());
            Ok(account)
        }
    }

    fn set_account(&mut self, index: u32, account: StacksAccount) {
        self.accounts.insert(index, account);
    }
}

pub fn init_module(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<AddressVersion>()?;
    m.add_class::<StacksAccount>()?;
    m.add_class::<StacksWallet>()?;
    m.add_class::<StacksPrivateKey>()?;
    Ok(())
}