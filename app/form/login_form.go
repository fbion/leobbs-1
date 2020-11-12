package form

type LoginForm struct {
	Username string `form:"username" binding:"required"`
	Password string `form:"forumpassword" binding:"required"`
}
