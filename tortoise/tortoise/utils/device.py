import torch
import psutil
import importlib

DEVICE_OVERRIDE = None
DEVICE_BATCH_SIZE_MAP = [(14, 16), (10,8), (7,4)]

from inspect import currentframe, getframeinfo
import gc

def do_gc():
    gc.collect()
    try:
        torch.cuda.empty_cache()
    except Exception as e:
        pass

def print_stats(collect=False):
    cf = currentframe().f_back
    msg = f'{getframeinfo(cf).filename}:{cf.f_lineno}'

    if collect:
        do_gc()

    tot = torch.cuda.get_device_properties(0).total_memory / (1024 ** 3)
    res = torch.cuda.memory_reserved(0) / (1024 ** 3)
    alloc = torch.cuda.memory_allocated(0) / (1024 ** 3)
    print("[{}] Total: {:.3f} | Reserved: {:.3f} | Allocated: {:.3f} | Free: {:.3f}".format( msg, tot, res, alloc, tot-res ))


def has_dml():
    loader = importlib.find_loader('torch_directml')
    if loader is None:
        return False
    
    import torch_directml
    return torch_directml.is_available()

def set_device_name(name):
    global DEVICE_OVERRIDE
    DEVICE_OVERRIDE = name

def get_device_name(attempt_gc=True):
    global DEVICE_OVERRIDE
    if DEVICE_OVERRIDE is not None and DEVICE_OVERRIDE != "":
        return DEVICE_OVERRIDE

    name = 'cpu'

    if torch.cuda.is_available():
        name = 'cuda'
        if attempt_gc:
            torch.cuda.empty_cache() # may have performance implications
    elif has_dml():
        name = 'dml'

    return name

def get_device(verbose=False):
    name = get_device_name()

    if verbose:
        if name == 'cpu':
            print("No hardware acceleration is available, falling back to CPU...")    
        else:
            print(f"Hardware acceleration found: {name}")

    if name == "dml":
        import torch_directml
        return torch_directml.device()

    return torch.device(name)

def get_device_vram( name=get_device_name() ):
    available = 1

    if name == "cuda":
        _, available = torch.cuda.mem_get_info()
    elif name == "cpu":
        available = psutil.virtual_memory()[4]

    return available / (1024 ** 3)

def get_device_batch_size(name=get_device_name()):
    vram = get_device_vram(name)

    if vram > 14:
        return 16
    elif vram > 10:
        return 8
    elif vram > 7:
        return 4
    """
    for k, v in DEVICE_BATCH_SIZE_MAP:
        if vram > k:
            return v
    """
    return 1

def get_device_count(name=get_device_name()):
    if name == "cuda":
        return torch.cuda.device_count()
    if name == "dml":
        import torch_directml
        return torch_directml.device_count()

    return 1


# if you're getting errors make sure you've updated your torch-directml, and if you're still getting errors then you can uncomment the below block
"""
if has_dml():
    _cumsum = torch.cumsum
    _repeat_interleave = torch.repeat_interleave
    _multinomial = torch.multinomial
    
    _Tensor_new = torch.Tensor.new
    _Tensor_cumsum = torch.Tensor.cumsum
    _Tensor_repeat_interleave = torch.Tensor.repeat_interleave
    _Tensor_multinomial = torch.Tensor.multinomial

    torch.cumsum = lambda input, *args, **kwargs: ( _cumsum(input.to("cpu"), *args, **kwargs).to(input.device) )
    torch.repeat_interleave = lambda input, *args, **kwargs: ( _repeat_interleave(input.to("cpu"), *args, **kwargs).to(input.device) )
    torch.multinomial = lambda input, *args, **kwargs: ( _multinomial(input.to("cpu"), *args, **kwargs).to(input.device) )
    
    torch.Tensor.new = lambda self, *args, **kwargs: ( _Tensor_new(self.to("cpu"), *args, **kwargs).to(self.device) )
    torch.Tensor.cumsum = lambda self, *args, **kwargs: ( _Tensor_cumsum(self.to("cpu"), *args, **kwargs).to(self.device) )
    torch.Tensor.repeat_interleave = lambda self, *args, **kwargs: ( _Tensor_repeat_interleave(self.to("cpu"), *args, **kwargs).to(self.device) )
    torch.Tensor.multinomial = lambda self, *args, **kwargs: ( _Tensor_multinomial(self.to("cpu"), *args, **kwargs).to(self.device) )
"""