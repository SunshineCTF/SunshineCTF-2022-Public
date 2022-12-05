package main
  
import "fmt"
  
// A basic main function that asks for a password and outputs a flag.
func main() {

	var query string;
	var password = "@t4r1_2600_l0v3r"

	fmt.Println("Please enter your password below:")
	fmt.Scanln(&query)

	if (query == password) {
		fmt.Println("Password accepted! Dispensing flag...")

		var message = "AF[LV^nG^hEQWl]M[TAhWPGGXRH"
		var flag = "2357111317192329313741434753"

		var strlen = len([]rune(message))

		for i := 0; i < strlen; i++ {
			var char_inp = int([]rune(message)[i])
			var char_flag = int([]rune(flag)[i % strlen])
			
			fmt.Printf("%s", string(rune(char_inp ^ char_flag)))
		}

		fmt.Println()
	} else {
		fmt.Println("Invalid password. Try again later!")
	}
}