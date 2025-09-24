import time
from typing import Callable


class Waiter:
    @staticmethod
    def wait_for(predicate: Callable[[], bool], timeout: float, poll: float = 0.1) -> bool:
        start = time.time()
        while time.time() - start < timeout:
            try:
                if predicate():
                    return True
            except Exception:
                pass
            time.sleep(poll)
        return False


