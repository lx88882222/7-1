from _typeshed import Incomplete
from collections.abc import Generator

STDOUT: int
STDERR: int

class SocketError(Exception): ...

NPIPE_ENDED: int

def read(socket, n: int = 4096): ...
def read_exactly(socket, n): ...
def next_frame_header(socket): ...
def frames_iter(socket, tty): ...
def frames_iter_no_tty(socket) -> Generator[Incomplete, None, None]: ...
def frames_iter_tty(socket) -> Generator[Incomplete, None, None]: ...
def consume_socket_output(frames, demux: bool = False): ...
def demux_adaptor(stream_id, data): ...