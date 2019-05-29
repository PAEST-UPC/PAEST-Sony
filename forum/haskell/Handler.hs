
{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE TypeFamilies #-}
{-# LANGUAGE TemplateHaskell #-}

module Handler
where
import Found
import Model

import Develop.DatFw
import Develop.DatFw.Handler
import Develop.DatFw.Template
import Develop.DatFw.Auth
import Develop.DatFw.Form
import Develop.DatFw.Form.Fields
import Data.Time
import Data.Maybe

import           Data.Text (Text)
import           Control.Monad.IO.Class   -- imports liftIO
import           Control.Monad

{---------------------------------------------------------------------
                TODO
---------------------------------------------------------------------}

themeForm :: AForm (HandlerFor Forum) Theme
themeForm =
    Theme <$> freq (checkM checkUserExists textField)
                   (withPlaceholder "Introduiu el nom de l'usuari responsable" "Nom del responsable")
                   Nothing
          <*> freq textField (withPlaceholder "Introduiu la categoria del tema" "Categoria") Nothing
          <*> freq textField (withPlaceholder "Introduiu el títol del tema" "Titol") Nothing
          <*> freq textareaField (withPlaceholder "Introduiu la descripció del tema" "Descripció") Nothing

checkUserExists :: Text -> HandlerFor Forum (Either Text Text)
checkUserExists uname = do
    users <- getsSite forumUsers
    case lookup uname users of
        Nothing -> pure $ Left "L'usuari no existeix"
        Just _  -> pure $ Right uname

getHomeR :: HandlerFor Forum Html
getHomeR = do
    -- Get model info
    db <- getsSite forumDb
    themes <- liftIO $ getThemeList db
    mbuser <- maybeAuthId
    tformw <- generateAFormPost themeForm
    -- Return HTML content
    defaultLayout $ do
        setTitle "Inici"
        $(widgetTemplFile "src/forum/templates/home.html")

postHomeR :: HandlerFor Forum Html
postHomeR = do
    user <- requireAuthId
    db <- getsSite forumDb
    (tformr, tformw) <- runAFormPost themeForm
    case tformr of
        FormSuccess newtheme -> do
            liftIO $ addTheme newtheme db
            redirectRoute HomeR []
        _ -> do
            themes <- liftIO $ getThemeList db
            let mbuser = Just user
            defaultLayout $(widgetTemplFile "src/forum/templates/home.html")


------------------------------------------------------------------

questionForm :: ThemeId -> AForm (HandlerFor Forum) Question
questionForm tid =
    Question <$> pure tid
          <*> liftToAForm requireAuthId
          <*> liftToAForm (liftIO getCurrentTime)
          <*> freq textField (withPlaceholder "Introduiu el títol de la pregunta" "Pregunta") Nothing
          <*> freq textareaField (withPlaceholder "Introduiu la descripció de la pregunta" "Descripció") Nothing

getThemeR :: ThemeId -> HandlerFor Forum Html
getThemeR tid = do
    -- Get model info
    db <- getsSite forumDb
    theme <- do
        mb <- liftIO $ getTheme tid db
        maybe notFound pure mb
    questions <- liftIO $ getQuestionList tid db
    mbuser <- maybeAuthId
    tformw <- generateAFormPost themeForm
    let isLeader = maybe False (tLeader theme ==) mbuser
    qformw <- generateAFormPost (questionForm tid)
    -- Return HTML content
    defaultLayout $ do
        setTitle "Tema"
        $(widgetTemplFile "src/forum/templates/theme.html")
    --fail "A completar per l'estudiant"

postThemeR :: ThemeId -> HandlerFor Forum Html
postThemeR tid = do
    user <- requireAuthId
    db <- getsSite forumDb
    theme <- do
        mb <- liftIO $ getTheme tid db
        maybe notFound pure mb
    (qformr, qformw) <- runAFormPost (questionForm tid)
    case qformr of
        FormSuccess newQuestion  -> do
            liftIO $ addQuestion newQuestion db
            redirectRoute (ThemeR tid) []
        _ -> do
            questions <- liftIO $ getQuestionList tid db
            let mbuser = Just user
            let isLeader = maybe False (tLeader theme ==) mbuser
            defaultLayout $(widgetTemplFile "src/forum/templates/theme.html")
    (tformr, tformw) <- runAFormPost themeForm
    case tformr of
        FormSuccess updatedTheme -> do
            liftIO $ updateTheme tid updatedTheme db
            redirectRoute (ThemeR tid) []
        _ -> do
            redirectRoute (ThemeR tid) []
    --fail "A completar per l'estudiant"

------------------------------------------------------------------

answerForm :: ThemeId -> QuestionId -> AForm (HandlerFor Forum) Answer
answerForm tid qid =
    Answer <$> pure qid
          <*> liftToAForm requireAuthId
          <*> liftToAForm (liftIO getCurrentTime)
          <*> freq textareaField (withPlaceholder "Introduiu la resposta" "Resposta") Nothing

getQuestionR :: ThemeId -> QuestionId -> HandlerFor Forum Html
getQuestionR tid qid = do
    -- Get model info
    db <- getsSite forumDb
    theme <- do
        mbt <- liftIO $ getTheme tid db
        maybe notFound pure mbt    
    question <- do
        mb <- liftIO $ getQuestion qid db
        maybe notFound pure mb
    answers <- liftIO $ getAnswerList qid db
    mbuser <- maybeAuthId 
    let isLeader = maybe False (tLeader theme ==) mbuser
    aformw <- generateAFormPost (answerForm tid qid)
    -- Return HTML content
    defaultLayout $ do
        setTitle "Pregunta"
        $(widgetTemplFile "src/forum/templates/question.html")
    --fail "A completar per l'estudiant"


postQuestionR :: ThemeId -> QuestionId -> HandlerFor Forum Html
postQuestionR tid qid = do
    user <- requireAuthId
    db <- getsSite forumDb
    theme <- do
        mbt <- liftIO $ getTheme tid db
        maybe notFound pure mbt
    question <- do
        mb <- liftIO $ getQuestion qid db
        maybe notFound pure mb
    answers <- liftIO $ getAnswerList qid db
    mbuser <- maybeAuthId 
    let isLeader = maybe False (tLeader theme ==) mbuser
    isDeleteQ <- isJust <$> lookupPostParam "delete-question"
    isDeleteA <- isJust <$> lookupPostParam "delete-answer"
    if isDeleteQ then do
       liftIO $ deleteQuestion qid db
       forM_ answers $ \ (id, answer) -> do
           liftIO $ deleteAnswer id db
       redirectRoute (ThemeR tid) []        
    else if isDeleteA then do
        Just aidt <- lookupPostParam "aid"
        let Just aid = fromPathPiece aidt
        liftIO $ deleteAnswer aid db
        redirectRoute (QuestionR tid qid) []
    else do
        (aformr, aformw) <- runAFormPost (answerForm tid qid)
        case aformr of
            FormSuccess newAnswer -> do
                liftIO $ addAnswer newAnswer db
                redirectRoute (QuestionR tid qid) []
            _ -> do
                let mbuser = Just user
                let isLeader = maybe False (tLeader theme ==) mbuser
                defaultLayout $(widgetTemplFile "src/forum/templates/question.html")
    --fail "A completar per l'estudiant"

