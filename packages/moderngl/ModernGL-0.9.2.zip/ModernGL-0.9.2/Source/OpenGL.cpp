#include "OpenGL.h"
#include "WindowsGL.h"

namespace OpenGL {

	bool LoadCoreOpenGLFunctions();

	const void * GetOpenGLFunction(const char * name) {
		const void * result = WindowsGL::GetWindowsFunctionFromOpenGL(name);
		if (result) {
			return result;
		}

		result = (const void *)WindowsGL::wglGetProcAddress(name);
		if (result) {
			return result;
		}

		int length = 0;
		while (name[length]) {
			++length;
		}
		
		char * guess = (char *)malloc(length + 4);
		memcpy(guess, name, length);

		guess[length + 0] = 'A';
		guess[length + 1] = 'R';
		guess[length + 2] = 'B';
		guess[length + 3] = 0;

		result = (const void *)WindowsGL::wglGetProcAddress(guess);
		if (result) {
			free(guess);
			return result;
		}

		guess[length + 0] = 'E';
		guess[length + 1] = 'X';
		guess[length + 2] = 'T';
		guess[length + 3] = 0;

		result = (const void *)WindowsGL::wglGetProcAddress(guess);
		if (result) {
			free(guess);
			return result;
		}

		free(guess);
		return 0;
	}

	bool __stdcall InitializeOpenGL() {
		if (!WindowsGL::InitializeWindowsGLModule()) {
			return false;
		}

		if (!LoadCoreOpenGLFunctions()) {
			return false;
		}

		return true;
	}

	bool LoadCoreOpenGLFunctions() {

		glLineWidth = (PROC_glLineWidth)GetOpenGLFunction("glLineWidth");
		glPointSize = (PROC_glPointSize)GetOpenGLFunction("glPointSize");
		glTexParameteri = (PROC_glTexParameteri)GetOpenGLFunction("glTexParameteri");
		glTexImage2D = (PROC_glTexImage2D)GetOpenGLFunction("glTexImage2D");
		glClear = (PROC_glClear)GetOpenGLFunction("glClear");
		glClearColor = (PROC_glClearColor)GetOpenGLFunction("glClearColor");
		glDisable = (PROC_glDisable)GetOpenGLFunction("glDisable");
		glEnable = (PROC_glEnable)GetOpenGLFunction("glEnable");
		glBlendFunc = (PROC_glBlendFunc)GetOpenGLFunction("glBlendFunc");
		glReadPixels = (PROC_glReadPixels)GetOpenGLFunction("glReadPixels");
		glGetError = (PROC_glGetError)GetOpenGLFunction("glGetError");
		glGetIntegerv = (PROC_glGetIntegerv)GetOpenGLFunction("glGetIntegerv");
		glGetString = (PROC_glGetString)GetOpenGLFunction("glGetString");
		glViewport = (PROC_glViewport)GetOpenGLFunction("glViewport");
		glBindTexture = (PROC_glBindTexture)GetOpenGLFunction("glBindTexture");
		glDeleteTextures = (PROC_glDeleteTextures)GetOpenGLFunction("glDeleteTextures");
		glGenTextures = (PROC_glGenTextures)GetOpenGLFunction("glGenTextures");
		glActiveTexture = (PROC_glActiveTexture)GetOpenGLFunction("glActiveTexture");
		glBindBuffer = (PROC_glBindBuffer)GetOpenGLFunction("glBindBuffer");
		glDeleteBuffers = (PROC_glDeleteBuffers)GetOpenGLFunction("glDeleteBuffers");
		glGenBuffers = (PROC_glGenBuffers)GetOpenGLFunction("glGenBuffers");
		glBufferData = (PROC_glBufferData)GetOpenGLFunction("glBufferData");
		glBufferSubData = (PROC_glBufferSubData)GetOpenGLFunction("glBufferSubData");
		glUnmapBuffer = (PROC_glUnmapBuffer)GetOpenGLFunction("glUnmapBuffer");
		glAttachShader = (PROC_glAttachShader)GetOpenGLFunction("glAttachShader");
		glCompileShader = (PROC_glCompileShader)GetOpenGLFunction("glCompileShader");
		glCreateProgram = (PROC_glCreateProgram)GetOpenGLFunction("glCreateProgram");
		glCreateShader = (PROC_glCreateShader)GetOpenGLFunction("glCreateShader");
		glDeleteProgram = (PROC_glDeleteProgram)GetOpenGLFunction("glDeleteProgram");
		glDeleteShader = (PROC_glDeleteShader)GetOpenGLFunction("glDeleteShader");
		glDisableVertexAttribArray = (PROC_glDisableVertexAttribArray)GetOpenGLFunction("glDisableVertexAttribArray");
		glEnableVertexAttribArray = (PROC_glEnableVertexAttribArray)GetOpenGLFunction("glEnableVertexAttribArray");
		glGetAttachedShaders = (PROC_glGetAttachedShaders)GetOpenGLFunction("glGetAttachedShaders");
		glGetAttribLocation = (PROC_glGetAttribLocation)GetOpenGLFunction("glGetAttribLocation");
		glGetProgramiv = (PROC_glGetProgramiv)GetOpenGLFunction("glGetProgramiv");
		glGetProgramInfoLog = (PROC_glGetProgramInfoLog)GetOpenGLFunction("glGetProgramInfoLog");
		glGetShaderiv = (PROC_glGetShaderiv)GetOpenGLFunction("glGetShaderiv");
		glGetShaderInfoLog = (PROC_glGetShaderInfoLog)GetOpenGLFunction("glGetShaderInfoLog");
		glGetUniformLocation = (PROC_glGetUniformLocation)GetOpenGLFunction("glGetUniformLocation");
		glLinkProgram = (PROC_glLinkProgram)GetOpenGLFunction("glLinkProgram");
		glShaderSource = (PROC_glShaderSource)GetOpenGLFunction("glShaderSource");
		glUseProgram = (PROC_glUseProgram)GetOpenGLFunction("glUseProgram");
		glUniform1f = (PROC_glUniform1f)GetOpenGLFunction("glUniform1f");
		glUniform2f = (PROC_glUniform2f)GetOpenGLFunction("glUniform2f");
		glUniform3f = (PROC_glUniform3f)GetOpenGLFunction("glUniform3f");
		glUniform4f = (PROC_glUniform4f)GetOpenGLFunction("glUniform4f");
		glUniform1i = (PROC_glUniform1i)GetOpenGLFunction("glUniform1i");
		glUniform2i = (PROC_glUniform2i)GetOpenGLFunction("glUniform2i");
		glUniform3i = (PROC_glUniform3i)GetOpenGLFunction("glUniform3i");
		glUniform4i = (PROC_glUniform4i)GetOpenGLFunction("glUniform4i");
		glUniformMatrix4fv = (PROC_glUniformMatrix4fv)GetOpenGLFunction("glUniformMatrix4fv");
		glVertexAttribPointer = (PROC_glVertexAttribPointer)GetOpenGLFunction("glVertexAttribPointer");
		glBindBufferBase = (PROC_glBindBufferBase)GetOpenGLFunction("glBindBufferBase");
		glBindFramebuffer = (PROC_glBindFramebuffer)GetOpenGLFunction("glBindFramebuffer");
		glDeleteFramebuffers = (PROC_glDeleteFramebuffers)GetOpenGLFunction("glDeleteFramebuffers");
		glGenFramebuffers = (PROC_glGenFramebuffers)GetOpenGLFunction("glGenFramebuffers");
		glFramebufferTexture2D = (PROC_glFramebufferTexture2D)GetOpenGLFunction("glFramebufferTexture2D");
		glGetFramebufferAttachmentParameteriv = (PROC_glGetFramebufferAttachmentParameteriv)GetOpenGLFunction("glGetFramebufferAttachmentParameteriv");
		glGenerateMipmap = (PROC_glGenerateMipmap)GetOpenGLFunction("glGenerateMipmap");
		glMapBufferRange = (PROC_glMapBufferRange)GetOpenGLFunction("glMapBufferRange");
		glBindVertexArray = (PROC_glBindVertexArray)GetOpenGLFunction("glBindVertexArray");
		glDeleteVertexArrays = (PROC_glDeleteVertexArrays)GetOpenGLFunction("glDeleteVertexArrays");
		glGenVertexArrays = (PROC_glGenVertexArrays)GetOpenGLFunction("glGenVertexArrays");
		glDrawArraysInstanced = (PROC_glDrawArraysInstanced)GetOpenGLFunction("glDrawArraysInstanced");
		glDrawElementsInstanced = (PROC_glDrawElementsInstanced)GetOpenGLFunction("glDrawElementsInstanced");
		glPrimitiveRestartIndex = (PROC_glPrimitiveRestartIndex)GetOpenGLFunction("glPrimitiveRestartIndex");
		glGetUniformBlockIndex = (PROC_glGetUniformBlockIndex)GetOpenGLFunction("glGetUniformBlockIndex");
		glDispatchCompute = (PROC_glDispatchCompute)GetOpenGLFunction("glDispatchCompute");

		return true;
	}

	bool __stdcall isglLineWidth() {
		return glLineWidth != 0;
	}

	bool __stdcall isglPointSize() {
		return glPointSize != 0;
	}

	bool __stdcall isglTexParameteri() {
		return glTexParameteri != 0;
	}

	bool __stdcall isglTexImage2D() {
		return glTexImage2D != 0;
	}

	bool __stdcall isglClear() {
		return glClear != 0;
	}

	bool __stdcall isglClearColor() {
		return glClearColor != 0;
	}

	bool __stdcall isglDisable() {
		return glDisable != 0;
	}

	bool __stdcall isglEnable() {
		return glEnable != 0;
	}

	bool __stdcall isglBlendFunc() {
		return glBlendFunc != 0;
	}

	bool __stdcall isglReadPixels() {
		return glReadPixels != 0;
	}

	bool __stdcall isglGetError() {
		return glGetError != 0;
	}

	bool __stdcall isglGetIntegerv() {
		return glGetIntegerv != 0;
	}

	bool __stdcall isglGetString() {
		return glGetString != 0;
	}

	bool __stdcall isglViewport() {
		return glViewport != 0;
	}

	bool __stdcall isglBindTexture() {
		return glBindTexture != 0;
	}

	bool __stdcall isglDeleteTextures() {
		return glDeleteTextures != 0;
	}

	bool __stdcall isglGenTextures() {
		return glGenTextures != 0;
	}

	bool __stdcall isglActiveTexture() {
		return glActiveTexture != 0;
	}

	bool __stdcall isglBindBuffer() {
		return glBindBuffer != 0;
	}

	bool __stdcall isglDeleteBuffers() {
		return glDeleteBuffers != 0;
	}

	bool __stdcall isglGenBuffers() {
		return glGenBuffers != 0;
	}

	bool __stdcall isglBufferData() {
		return glBufferData != 0;
	}

	bool __stdcall isglBufferSubData() {
		return glBufferSubData != 0;
	}

	bool __stdcall isglUnmapBuffer() {
		return glUnmapBuffer != 0;
	}

	bool __stdcall isglAttachShader() {
		return glAttachShader != 0;
	}

	bool __stdcall isglCompileShader() {
		return glCompileShader != 0;
	}

	bool __stdcall isglCreateProgram() {
		return glCreateProgram != 0;
	}

	bool __stdcall isglCreateShader() {
		return glCreateShader != 0;
	}

	bool __stdcall isglDeleteProgram() {
		return glDeleteProgram != 0;
	}

	bool __stdcall isglDeleteShader() {
		return glDeleteShader != 0;
	}

	bool __stdcall isglDisableVertexAttribArray() {
		return glDisableVertexAttribArray != 0;
	}

	bool __stdcall isglEnableVertexAttribArray() {
		return glEnableVertexAttribArray != 0;
	}

	bool __stdcall isglGetAttachedShaders() {
		return glGetAttachedShaders != 0;
	}

	bool __stdcall isglGetAttribLocation() {
		return glGetAttribLocation != 0;
	}

	bool __stdcall isglGetProgramiv() {
		return glGetProgramiv != 0;
	}

	bool __stdcall isglGetProgramInfoLog() {
		return glGetProgramInfoLog != 0;
	}

	bool __stdcall isglGetShaderiv() {
		return glGetShaderiv != 0;
	}

	bool __stdcall isglGetShaderInfoLog() {
		return glGetShaderInfoLog != 0;
	}

	bool __stdcall isglGetUniformLocation() {
		return glGetUniformLocation != 0;
	}

	bool __stdcall isglLinkProgram() {
		return glLinkProgram != 0;
	}

	bool __stdcall isglShaderSource() {
		return glShaderSource != 0;
	}

	bool __stdcall isglUseProgram() {
		return glUseProgram != 0;
	}

	bool __stdcall isglUniform1f() {
		return glUniform1f != 0;
	}

	bool __stdcall isglUniform2f() {
		return glUniform2f != 0;
	}

	bool __stdcall isglUniform3f() {
		return glUniform3f != 0;
	}

	bool __stdcall isglUniform4f() {
		return glUniform4f != 0;
	}

	bool __stdcall isglUniform1i() {
		return glUniform1i != 0;
	}

	bool __stdcall isglUniform2i() {
		return glUniform2i != 0;
	}

	bool __stdcall isglUniform3i() {
		return glUniform3i != 0;
	}

	bool __stdcall isglUniform4i() {
		return glUniform4i != 0;
	}

	bool __stdcall isglUniformMatrix4fv() {
		return glUniformMatrix4fv != 0;
	}

	bool __stdcall isglVertexAttribPointer() {
		return glVertexAttribPointer != 0;
	}

	bool __stdcall isglBindBufferBase() {
		return glBindBufferBase != 0;
	}

	bool __stdcall isglBindFramebuffer() {
		return glBindFramebuffer != 0;
	}

	bool __stdcall isglDeleteFramebuffers() {
		return glDeleteFramebuffers != 0;
	}

	bool __stdcall isglGenFramebuffers() {
		return glGenFramebuffers != 0;
	}

	bool __stdcall isglFramebufferTexture2D() {
		return glFramebufferTexture2D != 0;
	}

	bool __stdcall isglGetFramebufferAttachmentParameteriv() {
		return glGetFramebufferAttachmentParameteriv != 0;
	}

	bool __stdcall isglGenerateMipmap() {
		return glGenerateMipmap != 0;
	}

	bool __stdcall isglMapBufferRange() {
		return glMapBufferRange != 0;
	}

	bool __stdcall isglBindVertexArray() {
		return glBindVertexArray != 0;
	}

	bool __stdcall isglDeleteVertexArrays() {
		return glDeleteVertexArrays != 0;
	}

	bool __stdcall isglGenVertexArrays() {
		return glGenVertexArrays != 0;
	}

	bool __stdcall isglDrawArraysInstanced() {
		return glDrawArraysInstanced != 0;
	}

	bool __stdcall isglDrawElementsInstanced() {
		return glDrawElementsInstanced != 0;
	}

	bool __stdcall isglPrimitiveRestartIndex() {
		return glPrimitiveRestartIndex != 0;
	}

	bool __stdcall isglGetUniformBlockIndex() {
		return glGetUniformBlockIndex != 0;
	}

	bool __stdcall isglDispatchCompute() {
		return glDispatchCompute != 0;
	}


	PROC_glLineWidth glLineWidth;
	PROC_glPointSize glPointSize;
	PROC_glTexParameteri glTexParameteri;
	PROC_glTexImage2D glTexImage2D;
	PROC_glClear glClear;
	PROC_glClearColor glClearColor;
	PROC_glDisable glDisable;
	PROC_glEnable glEnable;
	PROC_glBlendFunc glBlendFunc;
	PROC_glReadPixels glReadPixels;
	PROC_glGetError glGetError;
	PROC_glGetIntegerv glGetIntegerv;
	PROC_glGetString glGetString;
	PROC_glViewport glViewport;
	PROC_glBindTexture glBindTexture;
	PROC_glDeleteTextures glDeleteTextures;
	PROC_glGenTextures glGenTextures;
	PROC_glActiveTexture glActiveTexture;
	PROC_glBindBuffer glBindBuffer;
	PROC_glDeleteBuffers glDeleteBuffers;
	PROC_glGenBuffers glGenBuffers;
	PROC_glBufferData glBufferData;
	PROC_glBufferSubData glBufferSubData;
	PROC_glUnmapBuffer glUnmapBuffer;
	PROC_glAttachShader glAttachShader;
	PROC_glCompileShader glCompileShader;
	PROC_glCreateProgram glCreateProgram;
	PROC_glCreateShader glCreateShader;
	PROC_glDeleteProgram glDeleteProgram;
	PROC_glDeleteShader glDeleteShader;
	PROC_glDisableVertexAttribArray glDisableVertexAttribArray;
	PROC_glEnableVertexAttribArray glEnableVertexAttribArray;
	PROC_glGetAttachedShaders glGetAttachedShaders;
	PROC_glGetAttribLocation glGetAttribLocation;
	PROC_glGetProgramiv glGetProgramiv;
	PROC_glGetProgramInfoLog glGetProgramInfoLog;
	PROC_glGetShaderiv glGetShaderiv;
	PROC_glGetShaderInfoLog glGetShaderInfoLog;
	PROC_glGetUniformLocation glGetUniformLocation;
	PROC_glLinkProgram glLinkProgram;
	PROC_glShaderSource glShaderSource;
	PROC_glUseProgram glUseProgram;
	PROC_glUniform1f glUniform1f;
	PROC_glUniform2f glUniform2f;
	PROC_glUniform3f glUniform3f;
	PROC_glUniform4f glUniform4f;
	PROC_glUniform1i glUniform1i;
	PROC_glUniform2i glUniform2i;
	PROC_glUniform3i glUniform3i;
	PROC_glUniform4i glUniform4i;
	PROC_glUniformMatrix4fv glUniformMatrix4fv;
	PROC_glVertexAttribPointer glVertexAttribPointer;
	PROC_glBindBufferBase glBindBufferBase;
	PROC_glBindFramebuffer glBindFramebuffer;
	PROC_glDeleteFramebuffers glDeleteFramebuffers;
	PROC_glGenFramebuffers glGenFramebuffers;
	PROC_glFramebufferTexture2D glFramebufferTexture2D;
	PROC_glGetFramebufferAttachmentParameteriv glGetFramebufferAttachmentParameteriv;
	PROC_glGenerateMipmap glGenerateMipmap;
	PROC_glMapBufferRange glMapBufferRange;
	PROC_glBindVertexArray glBindVertexArray;
	PROC_glDeleteVertexArrays glDeleteVertexArrays;
	PROC_glGenVertexArrays glGenVertexArrays;
	PROC_glDrawArraysInstanced glDrawArraysInstanced;
	PROC_glDrawElementsInstanced glDrawElementsInstanced;
	PROC_glPrimitiveRestartIndex glPrimitiveRestartIndex;
	PROC_glGetUniformBlockIndex glGetUniformBlockIndex;
	PROC_glDispatchCompute glDispatchCompute;

}
