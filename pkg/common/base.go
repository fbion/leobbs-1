package common

import (
	"database/sql"
	"gitee.com/leobbs/leobbs/app/orm_model"
	"gitee.com/leobbs/leobbs/app/skins"
	"github.com/flosch/pongo2/v4"
	"github.com/gin-gonic/gin"
	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
	"gorm.io/gorm/logger"
	"log"

	_ "github.com/mattn/go-sqlite3"
	"github.com/naoina/toml"
	"github.com/ztrue/tracerr"
	"go.uber.org/zap"
	"io/ioutil"
	"os"
	"time"
)

var (
	DB *gorm.DB
	Config *AppConfig

	Logger, _ = zap.NewProduction()
	Sugar *zap.SugaredLogger
)

type Msg struct {
	Msg string
}
type Umsg struct {
	Msg string
	Url string
}

type VBlogItem struct {
	aid            int
	content        sql.NullString
	publish_time   sql.NullString
	publish_status sql.NullInt64
}

/**
 * Logging error
 */
func LogError(err error) {
	Sugar.Error(tracerr.Sprint(tracerr.Wrap(err)))
}
/**
 * Logging info
 */
func LogInfo(msg string) {
	Sugar.Info(msg)
}
/**
 * close rows defer
 */
func CloseRowsDefer(rows *sql.Rows) {
	_ = rows.Close()
}
func ShowMessage(c *gin.Context, m *Msg) {



	pongoContext := pongo2.Context{
		"message":         m.Msg,
		"imagesurl": "/assets",
		"skin":      "leobbs",
		"hello":     "world",
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}

	c.HTML(200, "message.html",
		pongoContext)
	return
}


func ShowUMessage(c *gin.Context, m *Umsg) {

	pongoContext := pongo2.Context{
		"imagesurl": "/assets",
		"skin":      "leobbs",
		"message":         m.Msg,
		"url":             m.Url,
	}

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		pongoContext[tmpKey] = tmpV
	}

	c.HTML(200, "message.html",
		pongoContext)
	return
}

func GetMinutes() string {
	return time.Now().Format("200601021504")
}

func GetDB(config *AppConfig) *gorm.DB {

	newLogger := logger.New(
		log.New(os.Stdout, "\r\n", log.LstdFlags), // io writer
		logger.Config{
			SlowThreshold: time.Second,   // Slow SQL threshold
			LogLevel:      logger.Info, // Log level
			Colorful:      false,         // Disable color
		},
	)


	db, err := gorm.Open(sqlite.Open(config.Dbdsn), &gorm.Config{
		Logger: newLogger,
	})

	if err != nil {
		LogError(err)
	}
	err = db.AutoMigrate(&orm_model.Article{})
	if err != nil {
		LogError(err)
	}
	err = db.AutoMigrate(&orm_model.Member{})
	if err != nil {
		LogError(err)
	}

	err = db.AutoMigrate(&orm_model.Category{})
	if err != nil {
		LogError(err)
	}

	err = db.AutoMigrate(&orm_model.Forum{})
	if err != nil {
		LogError(err)
	}

	err = db.AutoMigrate(&orm_model.Topic{})
	if err != nil {
		LogError(err)
	}
	err = db.AutoMigrate(&orm_model.Post{})
	if err != nil {
		LogError(err)
	}


	return db
}


func InitApp() {

	//异步刷新日志
	defer func() {
		_ = Logger.Sync()
	}()

	Sugar = Logger.Sugar()


	Config = GetConfig()
	DB = GetDB(Config)
}
type AppConfig struct {
	Dbdsn          string
	Admin_user       []string
	Site_name        string
	Site_description string
	Key_of_encrypt string
	ObjectStorage    struct {
		Aws_access_key_id     string
		Aws_secret_access_key string
		Aws_region            string
		Aws_bucket            string
		Cdn_url               string
	}
	Email struct{
		Smtp_host string
		Smtp_port string
		Username string
		Password string
	}
}

func GetConfig() *AppConfig {
	_cm := "GetConfig@pkg/common/base"

	configFilePath := "./vol/config.toml"
	osEnvConfigFilePath := os.Getenv("LEOBBS_CONFIG_FILE")
	if osEnvConfigFilePath != "" {
		configFilePath = osEnvConfigFilePath
		Sugar.Infof("环境变量中有配置文件路径: LEOBBS_CONFIG_FILE: %s", osEnvConfigFilePath)
	}
	f, err := os.Open(configFilePath)
	if err != nil {
		if os.IsNotExist(err) {
			panic("默认配置文件不存在: "+ configFilePath +
				"， 您需要设置配置文件，位于./vol/config.toml, 如果需要指定其他位置，" +
				" 可以配置环境变量 LEOBBS_CONFIG_FILE=./vol/config.toml [记得替换成你自己的配置文件位置]")
		}
		panic(err)
	}
	defer f.Close()
	buf, err := ioutil.ReadAll(f)
	if err != nil {
		panic(err)
	}
	var config AppConfig
	if err := toml.Unmarshal(buf, &config); err != nil {
		Sugar.Infof(_cm + " error: %v", err)
	}
	return &config
}
