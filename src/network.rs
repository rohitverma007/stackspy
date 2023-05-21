use pyo3::prelude::*;
use stacks_rs::{StacksMainnet as StacksMainnetInner, StacksTestnet as StacksTestnetInner, StacksMocknet as StacksMocknetInner, Network};

#[pyclass]
pub struct StacksMainnet {
    inner: StacksMainnetInner,
}

#[pymethods]
impl StacksMainnet {
    #[new]
    fn new() -> Self {
        StacksMainnet {
            inner: StacksMainnetInner::new(),
        }
    }

    fn version(&self) -> u8 {
        self.inner.version() as u8
    }

    fn chain_id(&self) -> u32 {
        self.inner.chain_id() as u32
    }

    fn base_url(&self) -> String {
        self.inner.base_url()
    }
}

#[pyclass]
pub struct StacksTestnet {
    inner: StacksTestnetInner,
}

#[pymethods]
impl StacksTestnet {
    #[new]
    fn new() -> Self {
        StacksTestnet {
            inner: StacksTestnetInner::new(),
        }
    }

    fn version(&self) -> u8 {
        self.inner.version() as u8
    }

    fn chain_id(&self) -> u32 {
        self.inner.chain_id() as u32
    }

    fn base_url(&self) -> String {
        self.inner.base_url()
    }
}

#[pyclass]
pub struct StacksMocknet {
    inner: StacksMocknetInner,
}

#[pymethods]
impl StacksMocknet {
    #[new]
    fn new() -> Self {
        StacksMocknet {
            inner: StacksMocknetInner::new(),
        }
    }

    fn version(&self) -> u8 {
        self.inner.version() as u8
    }

    fn chain_id(&self) -> u32 {
        self.inner.chain_id() as u32
    }

    fn base_url(&self) -> String {
        self.inner.base_url()
    }
}

pub fn init_module(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<StacksMainnet>()?;
    m.add_class::<StacksTestnet>()?;
    m.add_class::<StacksMocknet>()?;

    Ok(())
}