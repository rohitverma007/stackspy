use pyo3::prelude::*;
mod network;
mod wallet;
mod transaction;

#[pymodule]
fn stackspy(_py: Python, m: &PyModule) -> PyResult<()> {
    wallet::init_module(_py, m)?;
    network::init_module(_py, m)?;
    transaction::init_module(_py, m)?;
    Ok(())
}