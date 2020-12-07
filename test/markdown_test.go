package test

import (
	"fmt"
	"testing"
)
import "github.com/russross/blackfriday/v2"

func TestMarkdownConvert(t *testing.T) {
	input := `
hello
### things will go on

I am the best 

* hello
* i 
* am 
* good
`
	output := blackfriday.Run([]byte(input))

	fmt.Printf("input: %s, out: %s", input, output)
}