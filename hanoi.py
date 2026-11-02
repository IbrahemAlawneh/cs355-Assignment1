import sys
from typing import List, Tuple

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")


def hanoi_recursive(
    n: int,
    source: str = 'A',
    destination: str = 'C',
    auxiliary: str = 'B'
) -> List[Tuple[int, str, str]]:

    moves: List[Tuple[int, str, str]] = []

    def _solve(k: int, src: str, dest: str, aux: str) -> None:
        if k <= 0:
            return
        if k == 1:
            moves.append((1, src, dest))
            return
        _solve(k - 1, src, aux, dest)
        moves.append((k, src, dest))
        _solve(k - 1, aux, dest, src)

    _solve(n, source, destination, auxiliary)
    return moves


def _make_legal_move(
    tower1: List[int],
    tower2: List[int],
    name1: str,
    name2: str
) -> Tuple[int, str, str]:

    if not tower1:
        disk = tower2.pop()
        tower1.append(disk)
        return (disk, name2, name1)
    elif not tower2:
        disk = tower1.pop()
        tower2.append(disk)
        return (disk, name1, name2)
    elif tower1[-1] > tower2[-1]:
        disk = tower2.pop()
        tower1.append(disk)
        return (disk, name2, name1)
    else:
        disk = tower1.pop()
        tower2.append(disk)
        return (disk, name1, name2)


def hanoi_iterative(
    n: int,
    source_name: str = 'A',
    destination_name: str = 'C',
    auxiliary_name: str = 'B'
) -> List[Tuple[int, str, str]]:

    if n <= 0:
        return []

    moves: List[Tuple[int, str, str]] = []

    source: List[int] = list(range(n, 0, -1))
    destination: List[int] = []
    auxiliary: List[int] = []

    src_name = source_name
    dest_name = destination_name
    aux_name = auxiliary_name

    if n % 2 == 0:
        dest_name, aux_name = aux_name, dest_name
        destination, auxiliary = auxiliary, destination

    total_moves = (2 ** n) - 1

    for step in range(1, total_moves + 1):
        remainder = step % 3
        if remainder == 1:
            move = _make_legal_move(source, destination, src_name, dest_name)
        elif remainder == 2:
            move = _make_legal_move(source, auxiliary, src_name, aux_name)
        else:
            move = _make_legal_move(auxiliary, destination, aux_name, dest_name)
        moves.append(move)

    return moves


def print_moves(moves: List[Tuple[int, str, str]]) -> None:
    for idx, (disk, src, dst) in enumerate(moves, 1):
        print(f"  Step {idx:2d}: Move disk {disk} from {src} -> {dst}")


def main() -> None:
    n = 3
    print("=" * 60)
    print(f"حل مسألة أبراج هانوي لعدد {n} أقراص")
    print(f"الحد الأدنى لعدد الحركات = 2^{n} - 1 = {(2**n) - 1}")
    print("=" * 60)

    print("\n[1] الحل باستخدام العودية (Recursion):")
    recursive_moves = hanoi_recursive(n, 'A', 'C', 'B')
    print_moves(recursive_moves)

    print("\n[2] الحل باستخدام التكرار (Iteration):")
    iterative_moves = hanoi_iterative(n, 'A', 'C', 'B')
    print_moves(iterative_moves)

    assert recursive_moves == iterative_moves, "Error: Moves do not match!"
    print("\n[SUCCESS] كلا الحلين (العودي والتكراري) أنتجا نفس الحركات الصحيحة تماماً بنجاح.")


if __name__ == "__main__":
    main()
