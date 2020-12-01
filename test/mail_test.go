package test

import (
	"crypto/tls"
	"gopkg.in/gomail.v2"
)



func main() {
	d :=  gomail.Dialer{Host: "localhost", Port: 25}
	d.TLSConfig = &tls.Config{InsecureSkipVerify: true}
	m := gomail.NewMessage()
	m.SetHeader("From", "no-reply@mx.leobbs.org")
	m.SetHeader("To", "netroby@qq.com")
	m.SetHeader("Subject", "Hello!")
	m.SetBody("text/plain", "Hello ")
	if err := d.DialAndSend(m); err != nil {
		panic(err)
	}
}