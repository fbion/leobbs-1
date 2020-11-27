package passwd_utils

import (
	"encoding/hex"
	"golang.org/x/crypto/bcrypt"
	"golang.org/x/crypto/blake2b"
)

func HashPassword(password string) (hashStr string, passwdStr string,  err error) {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), 14)
	hashStr = string(bytes)

	h := blake2b.Sum512([]byte(password + hashStr))
	passwdStr = hex.EncodeToString(h[:])
	return hashStr, passwdStr, nil

}

// passwdStr是数据库保存的密码，它是被加密过的
// password 是用户输入的密码
// hash 是数据库存储的密码hash
func CheckPasswordHash(passwdStr, password,  hash string) (bool, error) {

	h := blake2b.Sum512([]byte(password + hash))

	computedPasswdStr := hex.EncodeToString(h[:])

	return computedPasswdStr == passwdStr, nil
}
