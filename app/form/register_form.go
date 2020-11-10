package form

type RegisterForm struct {
	Username string `form:"inmembername" binding:"required"`
	Email string `form:"emailaddress" binding:"required"`
	Password string `form:"password" binding:"required"`
	Password2 string `form:"password2" binding:"required"`

}
