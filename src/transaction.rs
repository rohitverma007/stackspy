use pyo3::prelude::*;
use pyo3::wrap_pyfunction;
use crate::network::StacksMainnet;
use stacks_rs::transaction;
use secp256k1::SecretKey;
use crate::wallet::StacksPrivateKey;
use pyo3::exceptions::PyValueError;
use stacks_rs::transaction::PostConditions;
use crate::transaction::transaction::Error;

#[pyclass]
pub struct STXTokenTransfer {
    pub inner: transaction::STXTokenTransfer
}

#[pymethods]
impl STXTokenTransfer {
    #[new]
    pub fn new(
        recipient: &str,
        sender_key: StacksPrivateKey,
        amount: u64,
        nonce: u64,
        fee: u64,
        network: StacksMainnet,
        anchor_mode: transaction::AnchorMode,
        memo: &str,
        post_condition_mode: transaction::PostConditionMode,
        post_conditions: transaction::PostConditions,
        sponsored: bool,
    ) -> Self {
        let inner = transaction::STXTokenTransfer::new(
            recipient,
            sender_key.get_inner_sec_key(),
            amount,
            nonce,
            fee,
            network,
            anchor_mode,
            memo,
            post_condition_mode,
            post_conditions,
            sponsored,
        );
        STXTokenTransfer { inner }
    }

    // WIP:
    pub fn sign(&mut self) -> Result<transaction::StacksTransaction, transaction::Error> {
        let mut signer = transaction::TransactionSigner::new(&mut self.inner.transaction)
        .map_err(|e| PyErr::new::<pyo3::exceptions::PyException, _>(format!("{}", e)))?;
    
        signer.sign_origin(&self.inner.sender_key)
            .map_err(|e| PyErr::new::<pyo3::exceptions::PyException, _>(format!("{}", e)))?;
        
        Ok(self.inner.transaction.clone())
    }
}

pub fn init_module(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<transaction::AnchorMode>()?;
    m.add_class::<transaction::PostConditionMode>()?;
    m.add_class::<transaction::PostConditions>()?;
    m.add_class::<STXTokenTransfer>()?;
    Ok(())
}