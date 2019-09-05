package main

import (
	"database/sql"
	"github.com/rs/zerolog/log"

	//	"github.com/fvbock/endless"
	"github.com/gin-gonic/contrib/sessions"
	"github.com/gin-gonic/gin"
)

var (
	Config    *appConfig
	DB        *sql.DB
)

func main() {

	Config = GetConfig()
	DB = GetDB(Config)

	r := gin.Default()
	r.Static("/assets", "./vol/assets")
	store := sessions.NewCookieStore([]byte("gssecret"))
	r.Use(sessions.Sessions("mysession", store))
	r.LoadHTMLGlob("./vol/templates/*.html")

	fc := new(FrontController)
	r.GET("/", fc.HomeCtr)
	r.GET("/ws", fc.WsCtr)

/*
	apiCtrl := new(APIController)
	api := r.Group("/api")
	{
		api.HEAD("/", apiCtrl.HomeCtr)
		api.POST("/list", apiCtrl.ListCtr)
		api.POST("/login", apiCtrl.LoginCtr)
		api.POST("/logout", apiCtrl.LogoutCtr)
		api.POST("/file-upload", apiCtrl.FileUpload)
		api.POST("/save-blog-add", apiCtrl.SaveBlogAddCtr)
		api.POST("/save-blog-edit", apiCtrl.SaveBlogEditCtr)
	}*/
	log.Info().Msg("Server listen on :8083")
	err := r.Run(":8083")
	if err != nil {
		LogError(err)
	}
	//endless.ListenAndServe(":8080", r)
}
