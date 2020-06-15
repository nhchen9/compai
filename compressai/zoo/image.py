from torch.hub import load_state_dict_from_url

from compressai.models import (FactorizedPrior,
                               ScaleHyperprior,
                               MeanScaleHyperprior,
                               JointAutoregressiveHierarchicalPriors)

__all__ = [
    'bmshj2018_factorized',
    'bmshj2018_hyperprior',
    'mbt2018',
    'mbt2018_mean',
]

model_architectures = {
    'bmshj2018-factorized': FactorizedPrior,
    'bmshj2018-hyperprior': ScaleHyperprior,
    'mbt2018-mean': MeanScaleHyperprior,
    'mbt2018': JointAutoregressiveHierarchicalPriors,
}

root_url = 'https://compressai.s3.amazonaws.com/models/v1'
model_urls = {
    'bmshj2018-factorized': {
        'mse': {
            1: f'{root_url}/bmshj2018-factorized-prior-1-446d5c7f.pth.tar',
            2: f'{root_url}/bmshj2018-factorized-prior-2-87279a02.pth.tar',
            3: f'{root_url}/bmshj2018-factorized-prior-3-5c6f152b.pth.tar',
            4: f'{root_url}/bmshj2018-factorized-prior-4-1ed4405a.pth.tar',
            5: f'{root_url}/bmshj2018-factorized-prior-5-866ba797.pth.tar',
            6: f'{root_url}/bmshj2018-factorized-prior-6-9b02ea3a.pth.tar',
            7: f'{root_url}/bmshj2018-factorized-prior-7-6dfd6734.pth.tar',
            8: f'{root_url}/bmshj2018-factorized-prior-8-5232faa3.pth.tar',
        },
    },
    'bmshj2018-hyperprior': {
        'mse': {},
    },
    'mbt2018-mean': {
        'mse': {},
    },
    'mbt2018': {
        'mse': {},
    },
}

cfgs = {
    'bmshj2018-factorized': {
        1: (128, 192),
        2: (128, 192),
        3: (128, 192),
        4: (128, 192),
        5: (128, 192),
        6: (192, 320),
        7: (192, 320),
        8: (192, 320),
    },
    'bmshj2018-hyperprior': {
        1: (128, 192),
        2: (128, 192),
        3: (128, 192),
        4: (128, 192),
        5: (128, 192),
        6: (192, 320),
        7: (192, 320),
        8: (192, 320),
    },
    'mbt2018-mean': {
        1: (128, 192),
        2: (128, 192),
        3: (128, 192),
        4: (128, 192),
        5: (128, 192),
        6: (192, 320),
        7: (192, 320),
        8: (192, 320),
    },
    'mbt2018': {
        1: (192, 192),
        2: (192, 192),
        3: (192, 192),
        4: (192, 192),
        5: (192, 192),
        6: (192, 320),
        7: (192, 320),
        8: (192, 320),
    },
}


def _load_model(architecture,
                metric,
                quality,
                pretrained=False,
                progress=True,
                **kwargs):
    if architecture not in model_architectures:
        raise ValueError(f'Invalid architecture name "{architecture}"')

    if quality not in cfgs[architecture]:
        raise ValueError(f'Invalid quality value "{quality}"')

    if pretrained:
        if architecture not in model_urls or \
                metric not in model_urls[architecture] or \
                quality not in model_urls[architecture][metric]:
            raise RuntimeError('Pre-trained model not yet available')

        url = model_urls[architecture][metric][quality]
        state_dict = load_state_dict_from_url(url, progress=progress)
        model = model_architectures[architecture].from_state_dict(state_dict)
        return model

    model = model_architectures[architecture](*cfgs[architecture][quality], **kwargs)
    return model


def bmshj2018_factorized(quality,
                         metric='mse',
                         pretrained=False,
                         progress=True,
                         **kwargs):
    r"""Factorized Prior model from J. Balle, D. Minnen, S. Singh, S.J. Hwang,
    N. Johnston: `"Variational Image Compression with a Scale Hyperprior"
    <https://arxiv.org/abs/1802.01436>`_, Int Conf. on Learning Representations
    (ICLR), 2018.

    Args:
        quality (int): Quality levels (1: lowest, highest: 8)
        metric (str): Optimized metric, choose from ('mse')
        pretrained (bool): If True, returns a pre-trained model
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    if metric not in ('mse', ):
        raise ValueError(f'Invalid metric "{metric}"')

    if quality < 1 or quality > 8:
        raise ValueError(
            f'Invalid quality "{quality}", should be between (1, 8)')

    return _load_model('bmshj2018-factorized', metric, quality, pretrained,
                       progress, **kwargs)


def bmshj2018_hyperprior(quality,
                         metric='mse',
                         pretrained=False,
                         progress=True,
                         **kwargs):
    r"""Scale Hyperprior model from J. Balle, D. Minnen, S. Singh, S.J. Hwang,
    N. Johnston: `"Variational Image Compression with a Scale Hyperprior"
    <https://arxiv.org/abs/1802.01436>`_ Int. Conf. on Learning Representations
    (ICLR), 2018.

    Args:
        quality (int): Quality levels (1: lowest, highest: 8)
        metric (str): Optimized metric, choose from ('mse')
        pretrained (bool): If True, returns a pre-trained model
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    if metric not in ('mse', ):
        raise ValueError(f'Invalid metric "{metric}"')

    if quality < 1 or quality > 8:
        raise ValueError(
            f'Invalid quality "{quality}", should be between (1, 8)')

    return _load_model('bmshj2018-hyperprior', metric, quality, pretrained,
                       progress, **kwargs)


def mbt2018_mean(quality,
                 metric='mse',
                 pretrained=False,
                 progress=True,
                 **kwargs):
    r"""Scale Hyperprior with non zero-mean Gaussian conditionals from D.
    Minnen, J. Balle, G.D. Toderici: `"Joint Autoregressive and Hierarchical
    Priors for Learned Image Compression" <https://arxiv.org/abs/1809.02736>`_,
    Adv. in Neural Information Processing Systems 31 (NeurIPS 2018).

    Args:
        quality (int): Quality levels (1: lowest, highest: 8)
        metric (str): Optimized metric, choose from ('mse')
        pretrained (bool): If True, returns a pre-trained model
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    if metric not in ('mse', ):
        raise ValueError(f'Invalid metric "{metric}"')

    if quality < 1 or quality > 8:
        raise ValueError(
            f'Invalid quality "{quality}", should be between (1, 8)')

    return _load_model('mbt2018-mean', metric, quality, pretrained, progress,
                       **kwargs)


def mbt2018(quality, metric='mse', pretrained=False, progress=True, **kwargs):
    r"""Joint Autoregressive Hierarchical Priors model from D.
    Minnen, J. Balle, G.D. Toderici: `"Joint Autoregressive and Hierarchical
    Priors for Learned Image Compression" <https://arxiv.org/abs/1809.02736>`_,
    Adv. in Neural Information Processing Systems 31 (NeurIPS 2018).

    Args:
        quality (int): Quality levels (1: lowest, highest: 8)
        metric (str): Optimized metric, choose from ('mse')
        pretrained (bool): If True, returns a pre-trained model
        progress (bool): If True, displays a progress bar of the download to stderr
    """
    if metric not in ('mse', ):
        raise ValueError(f'Invalid metric "{metric}"')

    if quality < 1 or quality > 8:
        raise ValueError(
            f'Invalid quality "{quality}", should be between (1, 8)')

    return _load_model('mbt2018', metric, quality, pretrained, progress,
                       **kwargs)