#include <bits/stdc++.h>
/********important*********/
// include your cpp_debug_file.cpp location here
#include "/home/cpp_debug_file.cpp"

using namespace std;
#ifndef ONLINE_JUDGE
#define debug(x...)                 \
    cerr << "(" << __LINE__ << ") " \
         << "[" << #x << "] = [";   \
    _print(x);
#else
#define debug(x...)
#endif

int32_t main() {
    int a = 3;
    char c = 'z';
    string s = "asdf";
    vector<vector<pair<int, int>>> v{
        {{1, 2}, {2, 3}, {3, 4}},
        {{-1, 23}},
        {},
        {{42, 42}, {-1, -3}}};
    map<int, int> m;
    stack<int> s1;
    s1.push(1);
    s1.push(2);
    debug(s1);
    m[1] = 1;
    m[2] = 2;
    debug(a, c, s);
    debug(v);
    debug(a);
    debug(m);
}

/**
Output:
(28) [s1] = [{1,2}]
(31) [a, c, s] = [3, 'z', "asdf"]
(32) [v] = [{{(1,2),(2,3),(3,4)},{(-1,23)},{},{(42,42),(-1,-3)}}]
(33) [a] = [3]
(34) [m] = [{(1,1),(2,2)}]
***/
