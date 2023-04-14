// https://codeforces.com/contest/1679/problem/C solve

#include <bits/stdc++.h>
using namespace std;
#ifndef ONLINE_JUDGE
#include "/home/iinaamasum/cpp_file.cpp"
#else
#define dbg(x...)
#define case(tt)
#endif
#define endl "\n"
#define int long long
#define no cout << "NO" << endl
#define yes cout << "YES" << endl
#define all(_v) (_v).begin(), (_v).end()
#define rep(i, s, n) for (int i = s; i < n; ++i)
#define per(i, s, n) for (int i = n - 1; i >= s; --i)

class ST {
public:
    vector<int> tree, lazy;

    ST(){};
    ST(int n) {
        tree.resize(4 * n);
        lazy.resize(4 * n);
    }

    void build(int node, int lo, int hi, vector<int> &ar) {
        if (lo == hi) {
            tree[node] = ar[lo];
            return;
        }

        int mid = (lo + hi) >> 1;
        build(2 * node + 1, lo, mid, ar);
        build(2 * node + 2, mid + 1, hi, ar);
        tree[node] = tree[2 * node + 1] + tree[2 * node + 2];
    }

    void update(int node, int lo, int hi, int l, int r, int val) {
        // propagation
        if (lazy[node] != 0) {
            tree[node] = (hi - lo + 1) * lazy[node];

            // have child
            if (lo != hi) {
                lazy[2 * node + 1] = lazy[node];
                lazy[2 * node + 2] = lazy[node];
            }
            lazy[node] = 0;
        }

        // no overlap l..r lo..hi | lo..hi l..r
        if (r < lo or hi < l) {
            return;
        }

        // complete overlap l..lo..hi..r
        if (l <= lo and hi <= r) {
            tree[node] = (hi - lo + 1) * val;

            // have child, saving propagation
            if (lo != hi) {
                lazy[2 * node + 1] = val;
                lazy[2 * node + 2] = val;
            }
            return;
        }

        // partial overlap l..lo..r..hi | lo..l..hi..r
        int mid = (lo + hi) >> 1;
        update(2 * node + 1, lo, mid, l, r, val);
        update(2 * node + 2, mid + 1, hi, l, r, val);
        tree[node] = tree[2 * node + 1] + tree[2 * node + 2];
    }

    int query(int node, int lo, int hi, int l, int r) {
        // propagation
        if (lazy[node] != 0) {
            tree[node] = (hi - lo + 1) * lazy[node];

            // have child
            if (lo != hi) {
                lazy[2 * node + 1] = lazy[node];
                lazy[2 * node + 2] = lazy[node];
            }
            lazy[node] = 0;
        }

        // no overlap l..r lo..hi | lo..hi l..r
        if (r < lo or hi < l) {
            return 0;
        }

        // complete overlap l..lo..hi..r
        if (l <= lo and hi <= r) {
            return tree[node];
        }

        // partial overlap l..lo..r..hi
        int mid = (lo + hi) >> 1;
        int q1 = query(2 * node + 1, lo, mid, l, r);
        int q2 = query(2 * node + 2, mid + 1, hi, l, r);
        return q1 + q2;
    }
};

void testCase() {
    int n, q;
    cin >> n >> q;
    vector<int> row(n, 0), col(n, 0);
    ST st_row(n), st_col(n);
    st_row.build(0, 0, n - 1, row);
    st_col.build(0, 0, n - 1, col);
    map<int, int> m_row, m_col;
    while (q--) {
        int type;
        cin >> type;
        if (type == 1) {
            int x, y;
            cin >> x >> y;
            --x, --y;
            m_row[x]++, m_col[y]++;
            // t1 op
            if (m_row[x] == 1)
                st_row.update(0, 0, n - 1, x, x, 1);
            if (m_col[y] == 1)
                st_col.update(0, 0, n - 1, y, y, 1);
        } else if (type == 2) {
            int x, y;
            cin >> x >> y;
            --x, --y;
            m_row[x]--, m_col[y]--;
            // t2 op
            if (m_row[x] == 0)
                st_row.update(0, 0, n - 1, x, x, -1);
            if (m_col[y] == 0)
                st_col.update(0, 0, n - 1, y, y, -1);
        } else {
            int x, y, x_, y_;
            cin >> x >> y >> x_ >> y_;
            // t3 op
            --x, --y, --x_, --y_;
            int q1 = st_row.query(0, 0, n - 1, x, x_);
            int q2 = st_col.query(0, 0, n - 1, y, y_);
            // dbg(q1, q2);
            if (q1 == x_ - x + 1 or q2 == y_ - y + 1) {
                yes;
            } else {
                no;
            }
        }
    }
}

int32_t main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL), cout.tie(NULL);
    int t = 1;
    // cin >> t;
    rep(i, 1, t + 1) {
        // case(i);
        testCase();
    }
    return 0;
}
