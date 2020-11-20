package form

type NewTopicForm struct {
	Fid int64 `form:"fid" binding:"required"`
	Title string `form:"intopictitle" binding:"required"`
	Content string `form:"inpost" binding:"required"`
}
