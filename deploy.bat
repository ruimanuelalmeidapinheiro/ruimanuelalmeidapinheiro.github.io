@echo off
cls

echo ===================================================
echo STEP 1: Generating Local Sitemap and Key Cleanup
echo ===================================================
python generate_sitemap.py
if %ERRORLEVEL% NEQ 0 goto error

echo.
echo ===================================================
echo STEP 2: Committing and Pushing Changes to Git
echo ===================================================
git add .
git commit -m "Update sitemap, content changes, and key structure"
git push origin main
if %ERRORLEVEL% NEQ 0 goto error

echo.
echo ===================================================
echo STEP 3: Pausing for GitHub Pages Processing
echo ===================================================
echo Changes are pushed. Press any key AFTER your GitHub 
echo Pages site has finished deployment to send IndexNow.
pause

echo.
echo ===================================================
echo STEP 4: Submitting Manifest via IndexNow API
echo ===================================================
python submit_indexnow.py
if %ERRORLEVEL% NEQ 0 goto error

echo.
echo Pipeline finished successfully.
goto end

:error
echo.
echo ---------------------------------------------------
echo Pipeline stopped due to an error in the last stage.
echo ---------------------------------------------------
pause

:end