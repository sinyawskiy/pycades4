import re


async def parse_meta(lists: str):
    if len(lists):
        ret = dict((x, y) for x, y in re.findall(r'(emailAddress|E|C|L|O|CN|OU|STREET|SN|G)=([^,]*)', f'{lists} ,'))
        ret['raw'] = lists
        return ret

async def get_container_name(pk):
    result = ''
    try:
        result = pk.ContainerName
    except UnicodeDecodeError:
        pass
    return result

async def certificate_info(cert):
    cert_info = {}
    pk = cert.PrivateKey
    container_name = await get_container_name(pk)
    cert_info['privateKey'] = {
            'providerName': pk.ProviderName,
            'uniqueContainerName': pk.UniqueContainerName,
            'containerName': container_name,
    }
    algo = cert.PublicKey().Algorithm
    cert_info['algorithm'] = {
        'name': algo.FriendlyName,
        'val': algo.Value,
    }
    cert_info.update(
        {
            'valid': {
                'from': cert.ValidFromDate,
                'to': cert.ValidToDate,
            },
            'issuer': await parse_meta(cert.IssuerName),
            'subject': await parse_meta(cert.SubjectName),
            'thumbprint': cert.Thumbprint,
            'serialNumber': cert.SerialNumber,
            'hasPrivateKey': cert.HasPrivateKey()
        }
    )
    return cert_info
