@echo off
JARSIGNER -VERBOSE -SIGALG SHA1withRSA -digestalg SHA1 -KEYSTORE %1 -SIGNEDJAR %2  %3 %4 -STOREPASS %5
exit
@echo on