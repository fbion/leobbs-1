package main

import (
	"github.com/leobbs/leobbs/app/controller"
	"github.com/leobbs/leobbs/app/controller/account_controller"
	"github.com/leobbs/leobbs/app/controller/admin/admin_controller"
	"github.com/leobbs/leobbs/app/controller/admin/member_admin_controller"
	"github.com/leobbs/leobbs/app/controller/forum_controller"
	"github.com/leobbs/leobbs/app/controller/topic_controller"
	"github.com/leobbs/leobbs/pkg/common"
	"github.com/rs/zerolog/log"
	"gorm.io/gorm"

	//	"github.com/fvbock/endless"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"

	"github.com/cnmade/pongo2gin"
)

var (
	Config *common.AppConfig
	DB     *gorm.DB
)

func main() {
	//初始化应用
	common.InitApp()

	r := gin.Default()

	r.HTMLRender = pongo2gin.New(pongo2gin.RenderOptions{
		TemplateDir:   "views",
		ContentType:   "text/html; charset=utf-8",
		AlwaysNoCache: true,
	})

	r.Static("/assets", "./vol/assets")
	store := sessions.NewCookieStore([]byte("gssecret"))
	r.Use(sessions.Sessions("mysession", store))
	r.GET("/", controller.IndexAction)
	r.GET("/forum/:id", forum_controller.IndexAction)

	r.GET("/topic/:id", topic_controller.IndexAction)

	r.GET("/mp/newTopic", topic_controller.NewTopicAction)
	r.POST("/mp/saveNewTopic", topic_controller.SaveNewTopicAction)
	r.GET("/mp/editTopic", topic_controller.EditTopicAction)
	r.POST("/mp/saveEditTopic", topic_controller.SaveEditTopicAction)

	r.GET("/mp/newPost", topic_controller.NewPostAction)
	r.POST("/mp/saveNewPost", topic_controller.SaveNewPostAction)
	r.GET("/mp/editPost", topic_controller.EditPostAction)
	r.POST("/mp/saveEditPost", topic_controller.SaveEditPostAction)

	r.GET("/account/login", account_controller.LoginAction)
	r.POST("/account/doLogin", account_controller.DoLoginAction)
	r.GET("/account/logout", account_controller.LogoutAction)
	r.GET("/account/register", account_controller.RegisterAction)
	r.POST("/account/finishReg", account_controller.FinishRegAction)

	admin := r.Group("/admin")
	{
		admin.GET("/", admin_controller.Index)
		admin.GET("/member", member_admin_controller.IndexAction)
		admin.GET("/login", admin_controller.LoginAction)
	}
	log.Info().Msg("Server listen on :8083")
	err := r.Run(":8083")
	if err != nil {
		common.LogError(err)
	}
	//endless.ListenAndServe(":8080", r)
}
