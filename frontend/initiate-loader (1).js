// GitHub-safe JS loader for Lex Web UI
var Loader = ChatBotUiLoader.FullPageLoader;

var loaderOpts = {
  shouldIgnoreConfigWhenEmbedded: true,
  shouldLoadMinDeps: true,
};

var loader = new Loader(loaderOpts);

var chatbotUiConfig = {
  lex: {
    sessionAttributes: {
      userAgent: navigator.userAgent
    }
  }
};

loader
  .load(chatbotUiConfig)
  .then(function () { console.log('ChatBotUiLoader loaded'); })
  .catch(function (error) { console.error(error); });
