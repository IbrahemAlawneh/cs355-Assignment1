# مسألة أبراج هانوي (Towers of Hanoi)

تقرير تحليلي وتطبيقي شامل لمسألة أبراج هانوي بالحلين **العودي (Recursion)** و**التكراري (Iteration)** بلغة بايثون، متضمناً تحليل التعقيد الزمني والمكاني.

---

## 1. وصف المسألة والقواعد (Problem Description & Rules)

لدينا $n$ من الأقراص المرقمة $1, 2, 3, \dots, n$ وثلاثة أعمدة مسماة **A** (المصدر)، **B** (المساعد)، و **C** (الهدف).
جميع الأقراص موضوعة مبدئياً على العمود **A** مرتبة تنازلياً من الأكبر حجماً في الأسفل إلى الأصغر في الأعلى.

### القواعد:
1. لا يجوز وضع قرص كبير فوق قرص أصغر منه في أي وقت.
2. يتم تحريك قرص واحد فقط في كل خطوة، ويجب أن يكون القرص العلوي من العمود.
3. الهدف هو نقل كافة الأقراص من العمود **A** إلى العمود **C**.

الحد الأدنى لعدد الحركات هو:
$$M(n) = 2^n - 1$$

---

## 2. الخوارزمية المقترحة وخطوات الحل (Proposed Algorithm & Steps)

### أ) الخوارزمية العودية (Recursive Algorithm):
تعتمد على استراتيجية **"فرِّق تَسُد" (Divide and Conquer)**:
1. **حالة التوقف (Base Case):**
   * إذا كان $n = 1$: انقل القرص مباشرة من $A$ إلى $C$.
2. **الخطوات العودية (Recursive Steps):**
   * **الخطوة 1:** انقل $n - 1$ قرص من البرج $A$ إلى البرج المساعد $B$ باستخدام $C$ كبرج وسيط.
   * **الخطوة 2:** انقل القرص الأكبر (القرص $n$) مباشرة من $A$ إلى $C$.
   * **الخطوة 3:** انقل الـ $n - 1$ قرص من $B$ إلى $C$ باستخدام $A$ كبرج وسيط.

---

### ب) الخوارزمية التكرارية (Iterative Algorithm):
تعتمد على النمط الدوري الرياضي للحركات القانونية، باستخدام المكدسات (Stacks):
1. حساب إجمالي الحركات: $2^n - 1$.
2. إذا كان عدد الأقراص $n$ **زوجياً**، يتم تبديل وجهتي البرج المساعد وبرج الهدف في دورة الحركات.
3. التكرار لكل حركة $i$ من $1$ إلى $2^n - 1$:
   * إذا كان $i \pmod 3 == 1$: نفذ الحركة القانونية الوحيدة الممكنة بين **A** و **C**.
   * إذا كان $i \pmod 3 == 2$: نفذ الحركة القانونية الوحيدة الممكنة بين **A** و **B**.
   * إذا كان $i \pmod 3 == 0$: نفذ الحركة القانونية الوحيدة الممكنة بين **B** و **C**.
   *(الحركة القانونية: نقل القرص الأصغر فوق القرص الأكبر، أو نقله إلى العمود الفارغ).*

---

## 3. التطبيق البرمجي بلغة بايثون (Python Implementation)

الملف البرمجي جاهز ويعمل مباشرة في: [`hanoi.py`](./hanoi.py)

```python
from typing import List, Tuple

# 1. الحل باستخدام العودية (Recursion)
def hanoi_recursive(n: int, source: str = 'A', destination: str = 'C', auxiliary: str = 'B') -> List[Tuple[int, str, str]]:
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


# 2. الحل باستخدام التكرار (Iteration)
def _make_legal_move(tower1: List[int], tower2: List[int], name1: str, name2: str) -> Tuple[int, str, str]:
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


def hanoi_iterative(n: int, source_name: str = 'A', destination_name: str = 'C', auxiliary_name: str = 'B') -> List[Tuple[int, str, str]]:
    if n <= 0:
        return []

    moves: List[Tuple[int, str, str]] = []
    source = list(range(n, 0, -1))
    destination = []
    auxiliary = []

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
            moves.append(_make_legal_move(source, destination, src_name, dest_name))
        elif remainder == 2:
            moves.append(_make_legal_move(source, auxiliary, src_name, aux_name))
        else:
            moves.append(_make_legal_move(auxiliary, destination, aux_name, dest_name))

    return moves
```

---

## 4. مقارنة التعقيد (Complexity Comparison)

| وجه المقارنة | الحل العودي (Recursion) | الحل التكراري (Iteration) |
| :--- | :--- | :--- |
| **تعقيد الوقت (Time Complexity)** | $\mathcal{O}(2^n)$ | $\mathcal{O}(2^n)$ |
| **تعقيد المساحة (Space Complexity)** | $\mathcal{O}(n)$ | $\mathcal{O}(n)$ |
| **مصدر المساحة المستخدمة** | مكدس استدعاء الدوال (Call Stack Frames) | مكدسات الأقراص الصريحة (Explicit Stacks) |
| **سهولة التتبع والكتابة** | كود بسيط، مباشر وأنيق | منطق أطول ويحتاج إدارة للحالات |
| **خطر تجاوز المكدس (Stack Overflow)** | نعم (إذا كان $n$ كبيراً جداً وتجاوز حد بايثون) | غير معرّض لـ Stack Overflow |

### تفصيل التحليل:
* **التعقيد الزمني $\mathcal{O}(2^n)$:**
  الحد الأدنى لعدد الحركات هو $2^n - 1$. وحيث أن طباعة أو تنفيذ كل حركة يستغرق $\mathcal{O}(1)$، فلا يمكن لأي خوارزمية (سواء كانت عودية أو تكرارية) أن تستغرق وقتاً أقل من $\mathcal{O}(2^n)$.
* **التعقيد المكاني $\mathcal{O}(n)$:**
  - في الحل العودي: أقصى عمق لشجرة الاستدعاء العودي هو $n$ إطارات.
  - في الحل التكراري: مجموع عناصر الأبراج الثلاثة في أي لحظة هو بالضبط $n$ قرصاً.

---

