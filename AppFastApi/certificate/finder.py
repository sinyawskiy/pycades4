import pycades


async def store_data():
    store = pycades.Store()
    store.Open(pycades.CADESCOM_CONTAINER_STORE, pycades.CAPICOM_MY_STORE, pycades.CAPICOM_STORE_OPEN_MAXIMUM_ALLOWED)
    certs = store.Certificates
    assert (certs.Count != 0), "Certificates with private key not found"
    return certs


async def get_certificate(serial_number: str=None):
    certs = await store_data()
    cert = certs.Item(1)
    if serial_number:
        for i in range(1, certs.Count+1):
            cert = certs.Item(i)
            if cert.SerialNumber == serial_number:
                return cert
    return cert


async def signature_data(serial_number: str=None):
    certificate = await get_certificate(serial_number)
    signer = pycades.Signer()
    signer.Certificate = certificate
    signer.CheckCertificate = True
    return signer


async def signature_data_pin(pin: str, serial_number: str=None):
    certificate = await get_certificate(serial_number)
    signer = pycades.Signer()
    signer.Certificate = certificate
    signer.CheckCertificate = True
    signer.KeyPin = pin
    return signer
