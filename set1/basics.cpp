#include<iostream>
#include<vector>


//hex to byte array
std::vector<uint8_t> hexToBytes(std::string &hex){
    std::vector<uint8_t> bytes;
    for (int i = 0; i < hex.length(); i += 2){
        std::string byteString = hex.substr(i, 2);
        uint8_t byte = static_cast<uint8_t>(std::stoul(byteString, nullptr, 16)); //convert hex string to unsigned long
        bytes.push_back(byte);
    }
    return bytes;
}

//byte array to base64
std::string base64Encode(std::vector<uint8_t> &bytes){
    std::string base64Chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
    std::string base64;
    int i = 0;
    uint8_t byte1, byte2, byte3;
    while (i < bytes.size()){
        std::cout << "i:" << i << std::endl;
        byte1 = bytes[i++];
        std::cout << "byte1:" <<  byte1 << std::endl;
        base64 += base64Chars[byte1 >> 2];
        std::cout << "base64:" << base64 << std::endl;
        if (i == bytes.size()){
            base64 += base64Chars[(byte1 & 0x3) << 4];
            base64 += "==";
            break;
        }
        byte2 = bytes[i++];
        base64 += base64Chars[((byte1 & 0x3) << 4) | (byte2 >> 4)];
        if (i == bytes.size()){
            base64 += base64Chars[(byte2 & 0xF) << 2];
            base64 += "=";
            break;
        }
        byte3 = bytes[i++];
        base64 += base64Chars[((byte2 & 0xF) << 2) | (byte3 >> 6)];
        base64 += base64Chars[byte3 & 0x3F];
    }
    return base64;
}

int main() {
    std::string hex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d";
    std::string idiom = "Many hands make light work";
    std::vector<uint8_t> bytes = hexToBytes(hex);
    std::string base64 = base64Encode(bytes);
    
    for (int i = 0; i < bytes.size(); i++){
        std::cout << bytes[i];
    }
    std::cout << std::endl;
    std::cout << base64 << std::endl;
    return 0;
}