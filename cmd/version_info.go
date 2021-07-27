package main

import (
	"fmt"
	"github.com/leobbs/leobbs/pkg/common"
	"io/ioutil"
	"os/exec"
	"strings"
)

func main() {
	output, _ := exec.Command("git", "describe", "--tags", "--abbrev=0").Output()

	theVersion := strings.Trim(string(output), "\n")
	fmt.Println(theVersion)
	//_ = ioutil.WriteFile("./public/version.js", []byte(theVersion), 0755)

	var tmplStr = `package version
var BuildTag  = "%s"
var BuildNum  = "%s"`

	outStr := fmt.Sprintf(tmplStr, theVersion, common.GetMinutes())
	_ = ioutil.WriteFile("./pkg/version/version.go", []byte(outStr), 0755)
}
