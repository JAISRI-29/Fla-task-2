
import random
import itertools
import re
import fa_validators as F

results = []

def check(name, ok, detail=""):
    results.append(ok)
    print(("PASS " if ok else "FAIL ") + name +
          (f" [{detail}]" if detail else ""))


def words(alpha, maxlen):
    for n in range(maxlen + 1):
        for t in itertools.product(alpha, repeat=n):
            yield "".join(t)


def run_all():

    # PIN TESTING
    pin = F.make_pin()
    pin46 = F.make_pin_4or6()
    pin_ne = F.make_pin_not_all_equal()

    cnt = 0
    ok = True

    for w in words("07a ", 6):
        cnt += 1
        ok &= pin.accepts(
            [F.pin_class(c) for c in w]
        ) == bool(re.fullmatch(r"[0-9]{4}", w))

        ok &= pin46.accepts(
            [F.pin_class(c) for c in w]
        ) == bool(re.fullmatch(r"[0-9]{4}|[0-9]{6}", w))

    check("PIN 4-digit and 4-or-6 DFAs vs regex oracle",
          ok, f"{cnt} strings")

    ok = all(
        pin_ne.accepts(list(w)) ==
        (len(w) == 4 and len(set(w)) > 1)
        for n in range(6)
        for w in map(
            "".join,
            itertools.product("0123456789", repeat=n)
        )
    )

    check("PIN not-all-equal DFA vs rule", ok, "111111 strings")

    check(
        "PIN min-DFA sizes 6 / 8 / 35",
        (
            len(pin.states),
            len(pin46.states),
            len(F.minimise(pin_ne).states)
        ) == (6, 8, 35)
    )

    # CARD LOCK TESTING
    lock = F.make_lock()

    ok = all(
        lock.accepts(list(w)) == ("WWW" not in w)
        for w in words("CW", 12)
    )

    check("Card lock DFA vs no WWW rule", ok, "8191 strings")

    # PASSWORD TESTING
    comps, prod, mn = F.make_password()

    check(
        "Password product equals minimised product",
        F.equivalent(prod, mn),
        f"{len(prod.states)} -> {len(mn.states)} states"
    )

    def rule(w):
        return (
            8 <= len(w) <= 12
            and any('A' <= c <= 'Z' for c in w)
            and any('a' <= c <= 'z' for c in w)
            and any('0' <= c <= '9' for c in w)
            and not any(c.isspace() for c in w)
        )

    rnd = random.Random(2026)
    pool = "ABCxyz0189!@#$_- \t"

    ok = True
    n = 60000

    for _ in range(n):
        w = "".join(
            rnd.choice(pool)
            for _ in range(rnd.randint(0, 15))
        )

        cl = [F.pw_class(c) for c in w]

        ok &= (
            mn.accepts(cl) == rule(w)
            == prod.accepts(cl)
            == all(d.accepts(cl) for d in comps)
        )

    check(
        "Password component, product and minimised DFA",
        ok, f"{n} random strings"
    )

    edge = {
        "Aa1xxxx": False,
        "Aa1xxxxx": True,
        "Aa1xxxxxxxxx": True,
        "Aa1xxxxxxxxxx": False,
        "aaaaaaaa1": False,
        "AAAAAAAA1": False,
        "AaAaAaAa": False,
        "Aa1 xxxxx": False,
        "Aa1!xxxx": True
    }

    check(
        "Password boundary cases",
        all(
            mn.accepts([F.pw_class(c) for c in w]) == v
            for w, v in edge.items()
        )
    )

    # EMAIL TESTING
    nfa = F.make_email_nfa()
    d = nfa.to_dfa()
    m = F.minimise(d)

    check(
        "Email NFA/subset/minimal sizes 9 / 10 / 9",
        (len(nfa.states), len(d.states), len(m.states))
        == (9, 10, 9)
    )

    check(
        "Email subset DFA equals minimal DFA",
        F.equivalent(d, m)
    )

    ok = True
    cnt = 0

    for w in words("a1.-_+@", 7):
        cnt += 1
        cl = [F.em_class(c) for c in w]
        oracle = bool(F.EMAIL_RE.fullmatch(w))

        ok &= nfa.accepts(cl) == m.accepts(cl) == oracle

    check(
        "Email NFA and minimal DFA vs regex oracle",
        ok, f"{cnt} strings"
    )

    # EXAMPLE TESTING
    examples = {
        "pin": (
            pin, F.pin_class,
            ["5309", "0007", "2468", "9999", "1020", "3141"],
            ["530", "53091", "53o9", "53 09", "",
             "+5309", "5.309", "abcd"]
        ),

        "lock": (
            lock, None,
            ["", "C", "W", "WW", "WWC", "WCWCWW", "CWWCWW"],
            ["WWW", "CWWW", "WWWC", "WCWWW", "WWWWC"]
        ),

        "password": (
            mn, F.pw_class,
            ["Tiger#2026", "Mango9Pie", "aB3$efgh",
             "Chennai_88x", "Zq7!Zq7!Zq7!", "Trich1Tower"],
            ["tiger#2026", "TIGER#2026", "Tiger#Mango",
             "Tiger2026Tiger", "Tg#1", "Tiger #2026",
             "Abcdefgh1xyz9"]
        ),

        "email": (
            m, F.em_class,
            ["jaisri@srmist.edu.in",
             "ra2411026050248@srmist.edu.in",
             "web_dev+ngo@mail.org",
             "a-b.c@my-site.co", "x@y.io"],
            ["jaisri@srmist", ".jaisri@mail.com",
             "jaisri..s@mail.com", "jaisri@-srm.in",
             "jaisri@srm.c0m", "jaisri@@mail.com",
             "jaisri@srm.c"]
        )
    }

    for name, (dfa, cf, accepted, rejected) in examples.items():

        classify = (
            (lambda w, cf=cf: [cf(c) for c in w])
            if cf else
            (lambda w: list(w))
        )

        check(
            f"{name}: accepted and rejected examples",
            all(dfa.accepts(classify(w)) for w in accepted)
            and not any(
                dfa.accepts(classify(w)) for w in rejected
            )
        )

    print(f"\n{sum(results)}/{len(results)} checks passed")

    return all(results)


if __name__ == "__main__":
    raise SystemExit(0 if run_all() else 1)
