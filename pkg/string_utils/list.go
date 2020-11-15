package string_utils

func StringExistsInList(myStr string, target []string) bool {
	for _, v := range target {
		if myStr == v {
			return true
		}
	}
	return false
}
