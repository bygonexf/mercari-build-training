class Solution {
public:
    bool wordPattern(string pattern, string s) {
        unordered_map<string,char> p2s;
        unordered_map<char,string> s2p;

        stringstream ss(s);
        string tmp;
        for (char c : pattern) {
            if ((!(ss >> tmp)) || (s2p.count(c) == 1 && s2p[c] != tmp) || (p2s.count(tmp) == 1 && p2s[tmp] != c)) return false;
            s2p[c] = tmp;
            p2s[tmp] = c;
        }
        return (ss >> tmp) ? false : true;
    }
};