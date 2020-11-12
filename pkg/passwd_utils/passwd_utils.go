package passwd_utils

import (
	"gitee.com/leobbs/leobbs/pkg/common"
	"golang.org/x/crypto/bcrypt"
	"golang.org/x/crypto/blake2b"
)

func HashPassword(password string) (hashStr string, passwdStr string,  err error) {
	bytes, err := bcrypt.GenerateFromPassword([]byte(password), 14)
	hashStr = string(bytes)

	h, err := blake2b.New512([]byte(common.Config.Key_of_encrypt))
	if err != nil {
		return "", "", err
	}
	passwdStr = string(h.Sum([]byte(password + hashStr)))
	return hashStr, passwdStr, nil

}

// passwdStr是数据库保存的密码，它是被加密过的
// password 是用户输入的密码
// hash 是数据库存储的密码hash
func CheckPasswordHash(passwdStr, password,  hash string) (bool, error) {

	h, err := blake2b.New512([]byte(common.Config.Key_of_encrypt))
	if err != nil {
		return false, err
	}

	computedPasswdStr := string(h.Sum([]byte(password + hash)))

	return computedPasswdStr == passwdStr, nil
}
