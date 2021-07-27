package common

import (
	"github.com/flosch/pongo2/v4"
	"github.com/imdario/mergo"
	"github.com/leobbs/leobbs/app/skins"
	"github.com/leobbs/leobbs/pkg/version"
)

func Pongo2ContextAppend(ctx pongo2.Context, ctxAddition pongo2.Context) pongo2.Context {
	currentMethod := "Pongo2ContextAppend"
	err := mergo.Map(&ctx, ctxAddition);

	if err != nil {
		Sugar.Errorf(currentMethod + " merge pnogo2 context err: %v", err)
	}
	return ctx
}

func Pongo2ContextWithVersion(ctx pongo2.Context) pongo2.Context {
	outCtx := Pongo2ContextAppend(ctx, pongo2.Context{
		"BuildTag": version.BuildTag,
		"BuildNum": version.BuildNum,
		//"SiteKey": Config.HCaptchaSiteKey,
	//	"CaptchaEnabled": Config.CaptchaEnabled,
	})

	if Config.TongjiConfig.TongjiEnabled == 1 {
		outCtx = Pongo2ContextAppend(outCtx, pongo2.Context{
			"TongjiCode": Config.TongjiConfig.TongjiCode,
		})
	}

	//把模板变量也弄进来

	for tmpKey, tmpV := range skins.GetLeobbsSkin() {
		outCtx[tmpKey] = tmpV
	}
	Sugar.Infof("pongo2context: %+v", outCtx)
	return outCtx
}
