#include <iostream>
#include <algorithm>

using namespace std;

int main() {
    string s;
    getline(cin, s);  // Read input from user
    reverse(s.begin(), s.end());  // Reverse the string
    cout << s << endl;  
    return 0;
}
