@echo off


for %%i in (.\proto\*.proto) do (
echo server-----proto-- %%i
protoc --python_out=.\python\ -I proto %%i

)
echo over!
pause