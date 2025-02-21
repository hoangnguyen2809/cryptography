#include<iostream>
#include <sstream>
#include <iomanip>

std::string fixedXOR(std::string &hex1, std::string &hex2){
    if (hex1.length() != hex2.length()){
        std::cout << "Hex strings must be of equal length" << std::endl;
        return "";
    }

    std::stringstream result;
    for (int i = 0; i < hex1.length(); i+=2){
        std::string byte1 = hex1.substr(i, 2);
        std::string byte2 = hex2.substr(i, 2);
        int xorResult = std::stoi(byte1, nullptr, 16) ^ std::stoi(byte2, nullptr, 16);
        result << std::setw(2) << std::setfill('0') << std::hex << xorResult;
    }
    return result.str();
}


int main(){
    std::string hex1 = "1c0111001f010100061a024b53535009181c";
    std::string hex2 = "686974207468652062756c6c277320657965";
    std::string result;
    result = fixedXOR(hex1, hex2);
    std::cout << result << std::endl;
    return 0;
}