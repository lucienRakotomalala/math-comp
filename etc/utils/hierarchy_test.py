#!/usr/bin/python
# usage: hiearchy_test.py inputfile

import sys, argparse, collections

def print_hierarchy_test(G, test_cases):
    print ("(** Generated by etc/utils/hierarchy_test.py *)")
    print ("From mathcomp Require Import all.")

    print ("""
(* `check_join t1 t2 tjoin` assert that the join of `t1` and `t2` is `tjoin`. *)
Tactic Notation "check_join"
       open_constr(t1) open_constr(t2) open_constr(tjoin) :=
  let T1 := open_constr:(_ : t1) in
  let T2 := open_constr:(_ : t2) in
  match tt with
    | _ => unify ((id : t1 -> Type) T1) ((id : t2 -> Type) T2)
    | _ => fail "There is no join of" t1 "and" t2
  end;
  let Tjoin :=
    lazymatch T1 with
      | _ (_ ?Tjoin) => constr: (Tjoin)
      | _ ?Tjoin => constr: (Tjoin)
      | ?Tjoin => constr: (Tjoin)
    end
  in
  is_evar Tjoin;
  let tjoin' := type of Tjoin in
  lazymatch tjoin' with
    | tjoin => lazymatch tjoin with
                 | tjoin' => idtac
                 | _ => idtac tjoin'
               end
    | _ => fail "The join of" t1 "and" t2 "is" tjoin'
                "but is expected to be" tjoin
  end.
""")
    for x in G.keys():
        if x.rfind("Order") >= 0 or x.rfind("Norm") >= 0 or \
           x.rfind("Lmod") >= 0 or x.rfind("Splitting") >= 0 or \
           x.rfind("lgebra") >= 0 or x.rfind("FieldExt") >= 0 or \
           x.rfind("Vector") >= 0:
            print ("Local Notation \"" + x + ".type\" := (" + x + ".type _) (only parsing).")
    print ("")
    print ("Goal False.")
    for (x,y,z) in test_cases:
        print ("check_join " + x + ".type " + y + ".type " + z + ".type.")
    print ("Abort.")

def compute_least_common_children(G):
    tests=[]
    for pa, ch_a in G.items():
        for pb, ch_b in G.items():
            ch_c = ({pa} | ch_a) & ({pb} | ch_b) # common children
            for c in ch_c:
                ch_c = ch_c - G[c]
            if len(ch_c) == 1:
                tests.append((pa, pb, ch_c.pop()))
            elif 2 <= len(ch_c):
                print (pa, "and", pb, "have more than two least common children:", ch_c, ".", file=sys.stderr)
                sys.exit(1)
    return tests

def main():
    parser = argparse.ArgumentParser(description='Generate a check .v file \
                 for mathcomp structure hiearchies')
    parser.add_argument('graph', metavar='<graph>', nargs=1,
                        help='a file representing the hierarchy')
    args = parser.parse_args()
    G = {}
    with open(args.graph[0]) as f:
        for line in f:
            words = line.split()
            p = words.pop(0)
            G[p] = set(words)
    G = collections.OrderedDict(sorted(G.items()))
    print_hierarchy_test(G, compute_least_common_children(G))

if __name__ == "__main__":
    main()
