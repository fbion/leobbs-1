package passwd_utils

import (
	"encoding/hex"
	"fmt"
	"golang.org/x/crypto/blake2b"
	"testing"
)

func TestHashPassword(t *testing.T) {
	hstr, passwdStr, err := HashPassword("hello")
	fmt.Printf("hash: %s, passwd: %s, error: %v", hstr, passwdStr, err)
}

func TestBlake(t *testing.T) {

	blakeEncrypt("hello", "$2a$14$438s5qlEsupPptikcwHIY.sdfks/Xey4RJyJa")
	blakeEncrypt("what", "$2a$14$S00CEq6gLHSD8mhOrEGmL.sdfsd.0l4kUgVcODr.DmnpKsG")
	blakeEncrypt("fuck", "$2a$14$D5acYe2Jw7uL067tRrhIu.sxdf")
}

func blakeEncrypt(password, hashStr string) {
	h := blake2b.Sum512([]byte(password + hashStr))
	passwdStr := hex.EncodeToString(h[:])
	fmt.Println(passwdStr)
}