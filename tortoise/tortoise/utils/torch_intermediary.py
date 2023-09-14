"""
from bitsandbytes.nn import Linear8bitLt as Linear
from bitsandbytes.nn import StableEmbedding as Embedding
from bitsandbytes.optim.adam import Adam8bit as Adam
from bitsandbytes.optim.adamw import AdamW8bit as AdamW
"""
"""
from torch.nn import Linear
from torch.nn import Embedding
from torch.optim.adam import Adam
from torch.optim.adamw import AdamW
"""

"""
OVERRIDE_LINEAR = False
OVERRIDE_EMBEDDING = False
OVERRIDE_ADAM = False # True
OVERRIDE_ADAMW = False # True
"""

import os

USE_STABLE_EMBEDDING = False
try:
	OVERRIDE_LINEAR = False
	OVERRIDE_EMBEDDING = False
	OVERRIDE_ADAM = False
	OVERRIDE_ADAMW = False

	USE_STABLE_EMBEDDING = os.environ.get('BITSANDBYTES_USE_STABLE_EMBEDDING', '1' if USE_STABLE_EMBEDDING else '0') == '1'
	OVERRIDE_LINEAR = os.environ.get('BITSANDBYTES_OVERRIDE_LINEAR', '1' if OVERRIDE_LINEAR else '0') == '1'
	OVERRIDE_EMBEDDING = os.environ.get('BITSANDBYTES_OVERRIDE_EMBEDDING', '1' if OVERRIDE_EMBEDDING else '0') == '1'
	OVERRIDE_ADAM = os.environ.get('BITSANDBYTES_OVERRIDE_ADAM', '1' if OVERRIDE_ADAM else '0') == '1'
	OVERRIDE_ADAMW = os.environ.get('BITSANDBYTES_OVERRIDE_ADAMW', '1' if OVERRIDE_ADAMW else '0') == '1'
	
	if OVERRIDE_LINEAR or OVERRIDE_EMBEDDING or OVERRIDE_ADAM or OVERRIDE_ADAMW:
		import bitsandbytes as bnb
except Exception as e:
	OVERRIDE_LINEAR = False
	OVERRIDE_EMBEDDING = False
	OVERRIDE_ADAM = False
	OVERRIDE_ADAMW = False

if OVERRIDE_LINEAR:
	from bitsandbytes.nn import Linear8bitLt as Linear
else:
	from torch.nn import Linear

if OVERRIDE_EMBEDDING:
	if USE_STABLE_EMBEDDING:
		from bitsandbytes.nn import StableEmbedding as Embedding
	else:
		from bitsandbytes.nn.modules import Embedding as Embedding
else:
	from torch.nn import Embedding

if OVERRIDE_ADAM:
	from bitsandbytes.optim.adam import Adam8bit as Adam
else:
	from torch.optim.adam import Adam

if OVERRIDE_ADAMW:
	from bitsandbytes.optim.adamw import AdamW8bit as AdamW
else:
	from torch.optim.adamw import AdamW