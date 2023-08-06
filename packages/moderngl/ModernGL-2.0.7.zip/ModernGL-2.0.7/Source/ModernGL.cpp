#include "ModernGL.hpp"
#include "OpenGL.hpp"

#include <cstdio>
#include <cstring>
#include <cstdarg>
#include <malloc.h>

namespace {
	int defaultVertexArray;
	int defaultFramebuffer;
	int defaultProgram;

	int defaultTextureUnit;

	const int maxCompilerLog = 16 * 1024;
	char compilerLog[maxCompilerLog + 1];

	bool extensionActive = false;

	const char * errorMessage = 0;
}

namespace ModernGL {
	bool TestFunctions() {
		if (!OpenGL::isglActiveTexture()) {
			errorMessage = "glActiveTexture not loaded.";
			return false;
		}
		if (!OpenGL::isglAttachShader()) {
			errorMessage = "glAttachShader not loaded.";
			return false;
		}
		if (!OpenGL::isglBindBuffer()) {
			errorMessage = "glBindBuffer not loaded.";
			return false;
		}
		if (!OpenGL::isglBindBufferBase()) {
			errorMessage = "glBindBufferBase not loaded.";
			return false;
		}
		if (!OpenGL::isglBindFramebuffer()) {
			errorMessage = "glBindFramebuffer not loaded.";
			return false;
		}
		if (!OpenGL::isglBindTexture()) {
			errorMessage = "glBindTexture not loaded.";
			return false;
		}
		if (!OpenGL::isglBindVertexArray()) {
			errorMessage = "glBindVertexArray not loaded.";
			return false;
		}
		if (!OpenGL::isglBlendFunc()) {
			errorMessage = "glBlendFunc not loaded.";
			return false;
		}
		if (!OpenGL::isglBufferData()) {
			errorMessage = "glBufferData not loaded.";
			return false;
		}
		if (!OpenGL::isglBufferSubData()) {
			errorMessage = "glBufferSubData not loaded.";
			return false;
		}
		if (!OpenGL::isglClear()) {
			errorMessage = "glClear not loaded.";
			return false;
		}
		if (!OpenGL::isglClearColor()) {
			errorMessage = "glClearColor not loaded.";
			return false;
		}
		if (!OpenGL::isglCompileShader()) {
			errorMessage = "glCompileShader not loaded.";
			return false;
		}
		if (!OpenGL::isglCreateProgram()) {
			errorMessage = "glCreateProgram not loaded.";
			return false;
		}
		if (!OpenGL::isglCreateShader()) {
			errorMessage = "glCreateShader not loaded.";
			return false;
		}
		if (!OpenGL::isglDeleteBuffers()) {
			errorMessage = "glDeleteBuffers not loaded.";
			return false;
		}
		if (!OpenGL::isglDeleteFramebuffers()) {
			errorMessage = "glDeleteFramebuffers not loaded.";
			return false;
		}
		if (!OpenGL::isglDeleteProgram()) {
			errorMessage = "glDeleteProgram not loaded.";
			return false;
		}
		if (!OpenGL::isglDeleteShader()) {
			errorMessage = "glDeleteShader not loaded.";
			return false;
		}
		if (!OpenGL::isglDeleteTextures()) {
			errorMessage = "glDeleteTextures not loaded.";
			return false;
		}
		if (!OpenGL::isglDeleteVertexArrays()) {
			errorMessage = "glDeleteVertexArrays not loaded.";
			return false;
		}
		if (!OpenGL::isglDisable()) {
			errorMessage = "glDisable not loaded.";
			return false;
		}
		if (!OpenGL::isglDisableVertexAttribArray()) {
			errorMessage = "glDisableVertexAttribArray not loaded.";
			return false;
		}
		if (!OpenGL::isglDrawArraysInstanced()) {
			errorMessage = "glDrawArraysInstanced not loaded.";
			return false;
		}
		if (!OpenGL::isglDrawElementsInstanced()) {
			errorMessage = "glDrawElementsInstanced not loaded.";
			return false;
		}
		if (!OpenGL::isglEnable()) {
			errorMessage = "glEnable not loaded.";
			return false;
		}
		if (!OpenGL::isglEnableVertexAttribArray()) {
			errorMessage = "glEnableVertexAttribArray not loaded.";
			return false;
		}
		if (!OpenGL::isglFramebufferTexture2D()) {
			errorMessage = "glFramebufferTexture2D not loaded.";
			return false;
		}
		if (!OpenGL::isglGenBuffers()) {
			errorMessage = "glGenBuffers not loaded.";
			return false;
		}
		if (!OpenGL::isglGenerateMipmap()) {
			errorMessage = "glGenerateMipmap not loaded.";
			return false;
		}
		if (!OpenGL::isglGenFramebuffers()) {
			errorMessage = "glGenFramebuffers not loaded.";
			return false;
		}
		if (!OpenGL::isglGenTextures()) {
			errorMessage = "glGenTextures not loaded.";
			return false;
		}
		if (!OpenGL::isglGenVertexArrays()) {
			errorMessage = "glGenVertexArrays not loaded.";
			return false;
		}
		if (!OpenGL::isglGetAttachedShaders()) {
			errorMessage = "glGetAttachedShaders not loaded.";
			return false;
		}
		if (!OpenGL::isglGetAttribLocation()) {
			errorMessage = "glGetAttribLocation not loaded.";
			return false;
		}
		if (!OpenGL::isglGetError()) {
			errorMessage = "glGetError not loaded.";
			return false;
		}
		if (!OpenGL::isglGetFramebufferAttachmentParameteriv()) {
			errorMessage = "glGetFramebufferAttachmentParameteriv not loaded.";
			return false;
		}
		if (!OpenGL::isglGetIntegerv()) {
			errorMessage = "glGetIntegerv not loaded.";
			return false;
		}
		if (!OpenGL::isglGetProgramInfoLog()) {
			errorMessage = "glGetProgramInfoLog not loaded.";
			return false;
		}
		if (!OpenGL::isglGetProgramiv()) {
			errorMessage = "glGetProgramiv not loaded.";
			return false;
		}
		if (!OpenGL::isglGetShaderInfoLog()) {
			errorMessage = "glGetShaderInfoLog not loaded.";
			return false;
		}
		if (!OpenGL::isglGetShaderiv()) {
			errorMessage = "glGetShaderiv not loaded.";
			return false;
		}
		if (!OpenGL::isglGetString()) {
			errorMessage = "glGetString not loaded.";
			return false;
		}
		if (!OpenGL::isglGetStringi()) {
			errorMessage = "glGetStringi not loaded.";
			return false;
		}
		if (!OpenGL::isglGetUniformBlockIndex()) {
			errorMessage = "glGetUniformBlockIndex not loaded.";
			return false;
		}
		if (!OpenGL::isglGetUniformLocation()) {
			errorMessage = "glGetUniformLocation not loaded.";
			return false;
		}
		if (!OpenGL::isglLineWidth()) {
			errorMessage = "glLineWidth not loaded.";
			return false;
		}
		if (!OpenGL::isglLinkProgram()) {
			errorMessage = "glLinkProgram not loaded.";
			return false;
		}
		if (!OpenGL::isglMapBufferRange()) {
			errorMessage = "glMapBufferRange not loaded.";
			return false;
		}
		if (!OpenGL::isglPointSize()) {
			errorMessage = "glPointSize not loaded.";
			return false;
		}
		if (!OpenGL::isglPrimitiveRestartIndex()) {
			errorMessage = "glPrimitiveRestartIndex not loaded.";
			return false;
		}
		if (!OpenGL::isglReadPixels()) {
			errorMessage = "glReadPixels not loaded.";
			return false;
		}
		if (!OpenGL::isglShaderSource()) {
			errorMessage = "glShaderSource not loaded.";
			return false;
		}
		if (!OpenGL::isglTexImage2D()) {
			errorMessage = "glTexImage2D not loaded.";
			return false;
		}
		if (!OpenGL::isglTexParameteri()) {
			errorMessage = "glTexParameteri not loaded.";
			return false;
		}
		if (!OpenGL::isglUniform1f()) {
			errorMessage = "glUniform1f not loaded.";
			return false;
		}
		if (!OpenGL::isglUniform1i()) {
			errorMessage = "glUniform1i not loaded.";
			return false;
		}
		if (!OpenGL::isglUniform2f()) {
			errorMessage = "glUniform2f not loaded.";
			return false;
		}
		if (!OpenGL::isglUniform2i()) {
			errorMessage = "glUniform2i not loaded.";
			return false;
		}
		if (!OpenGL::isglUniform3f()) {
			errorMessage = "glUniform3f not loaded.";
			return false;
		}
		if (!OpenGL::isglUniform3i()) {
			errorMessage = "glUniform3i not loaded.";
			return false;
		}
		if (!OpenGL::isglUniform4f()) {
			errorMessage = "glUniform4f not loaded.";
			return false;
		}
		if (!OpenGL::isglUniform4i()) {
			errorMessage = "glUniform4i not loaded.";
			return false;
		}
		if (!OpenGL::isglUniformMatrix4fv()) {
			errorMessage = "glUniformMatrix4fv not loaded.";
			return false;
		}
		if (!OpenGL::isglUnmapBuffer()) {
			errorMessage = "glUnmapBuffer not loaded.";
			return false;
		}
		if (!OpenGL::isglUseProgram()) {
			errorMessage = "glUseProgram not loaded.";
			return false;
		}
		if (!OpenGL::isglVertexAttribPointer()) {
			errorMessage = "glVertexAttribPointer not loaded.";
			return false;
		}
		if (!OpenGL::isglViewport()) {
			errorMessage = "glViewport not loaded.";
			return false;
		}

		return true;
	}

	bool TestExtensions() {
		int extensions = 0;
		OpenGL::glGetIntegerv(OpenGL::GL_NUM_EXTENSIONS, &extensions);

		bool shader_storage_buffer_object = false;
		bool tessellation_shader = false;
		bool compute_shader = false;

		for (int i = 0; i < extensions; ++i) {
			const char * ext = (const char *)OpenGL::glGetStringi(OpenGL::GL_EXTENSIONS, i);
			if (!ext) {
				continue;
			}

			if (!shader_storage_buffer_object && !strcmp("GL_ARB_shader_storage_buffer_object", ext)) {
				shader_storage_buffer_object = true;
			}

			if (!tessellation_shader && !strcmp("GL_ARB_tessellation_shader", ext)) {
				tessellation_shader = true;
			}

			if (!compute_shader && !strcmp("GL_ARB_compute_shader", ext)) {
				compute_shader = true;
			}
		}

		if (!shader_storage_buffer_object) {
			return false;
		}

		if (!tessellation_shader) {
			return false;
		}
		
		if (!compute_shader) {
			return false;
		}

		if (!OpenGL::isglBindImageTexture()) {
			return false;
		}

		if (!OpenGL::isglDispatchCompute()) {
			return false;
		}

		return true;
	}

	bool InitializeModernGL(bool font) {
		// Initialize OpenGL
		if (!OpenGL::InitializeOpenGL()) {
			errorMessage = "InitializeOpenGL failed.";
			return false;
		}

		// Test all the gl functions
		if (!TestFunctions()) {
			return false;
		}

		// Test for better support
		extensionActive = TestExtensions();
		
		// Default blending
		OpenGL::glBlendFunc(OpenGL::GL_SRC_ALPHA, OpenGL::GL_ONE_MINUS_SRC_ALPHA);

		// Default primitive restart index
		OpenGL::glEnable(OpenGL::GL_PRIMITIVE_RESTART);
		OpenGL::glPrimitiveRestartIndex(-1);

		// Default VAO for GL_ELEMENT_ARRAY operations
		OpenGL::glGenVertexArrays(1, (OpenGL::GLuint *)&defaultVertexArray);
		OpenGL::glBindVertexArray(defaultVertexArray);

		// Default FBO and program
		OpenGL::glGetIntegerv(OpenGL::GL_DRAW_FRAMEBUFFER_BINDING, (OpenGL::GLint *)&defaultFramebuffer);
		OpenGL::glGetIntegerv(OpenGL::GL_CURRENT_PROGRAM, (OpenGL::GLint *)&defaultProgram);

		// Default texture unit for texture operations
		int maxTextureUnits = 1;
		OpenGL::glGetIntegerv(OpenGL::GL_MAX_TEXTURE_IMAGE_UNITS, (OpenGL::GLint *)&maxTextureUnits);
		defaultTextureUnit = maxTextureUnits - 1;

		return true;
	}

	Info GetInfo() {
		int major = 0;
		int minor = 0;
		int samples = 0;

		OpenGL::glGetIntegerv(OpenGL::GL_MAJOR_VERSION, &major);
		OpenGL::glGetIntegerv(OpenGL::GL_MINOR_VERSION, &minor);
		OpenGL::glGetIntegerv(OpenGL::GL_MAX_SAMPLES, &samples);
		const char * vendor = (const char *)OpenGL::glGetString(OpenGL::GL_VENDOR);
		const char * renderer = (const char *)OpenGL::glGetString(OpenGL::GL_RENDERER);

		if (!vendor) {
			vendor = "";
		}
		
		if (!renderer) {
			renderer = "";
		}

		Info tuple = {
			major,
			minor,
			samples,
			vendor,
			renderer,
		};

		return tuple;
	}

	const char * GetError() {
		if (errorMessage) {
			return errorMessage;
		}
		return "No Error";
	}

	void Viewport(int x, int y, int w, int h) {
		OpenGL::glViewport(x, y, w, h);
	}

	void Clear(unsigned char r, unsigned char g, unsigned char b, unsigned char a) {
		const float c = 1.0f / 255.0f;
		OpenGL::glClearColor(r * c, g * c, b * c, a * c);
		unsigned GL_ALL_BUFFER_BIT = 0;
		GL_ALL_BUFFER_BIT |= OpenGL::GL_DEPTH_BUFFER_BIT;
		GL_ALL_BUFFER_BIT |= OpenGL::GL_COLOR_BUFFER_BIT;
		OpenGL::glClear(GL_ALL_BUFFER_BIT);
	}

	void PointSize(float size) {
		OpenGL::glPointSize(size);
	}

	void LineSize(float size) {
		OpenGL::glLineWidth(size);
	}

	void EnableOnly(unsigned mask) {
		(mask & ENABLE_BLEND ? OpenGL::glEnable : OpenGL::glDisable)(OpenGL::GL_BLEND);
		(mask & ENABLE_CULL_FACE ? OpenGL::glEnable : OpenGL::glDisable)(OpenGL::GL_CULL_FACE);
		(mask & ENABLE_DEPTH_TEST ? OpenGL::glEnable : OpenGL::glDisable)(OpenGL::GL_DEPTH_TEST);
		(mask & ENABLE_MULTISAMPLE ? OpenGL::glEnable : OpenGL::glDisable)(OpenGL::GL_MULTISAMPLE);
	}

	void EnableBlend() {
		OpenGL::glEnable(OpenGL::GL_BLEND);
	}

	void DisableBlend() {
		OpenGL::glDisable(OpenGL::GL_BLEND);
	}

	void EnableCullFace() {
		OpenGL::glEnable(OpenGL::GL_CULL_FACE);
	}

	void DisableCullFace() {
		OpenGL::glDisable(OpenGL::GL_CULL_FACE);
	}

	void EnableDepthTest() {
		OpenGL::glEnable(OpenGL::GL_DEPTH_TEST);
	}

	void DisableDepthTest() {
		OpenGL::glDisable(OpenGL::GL_DEPTH_TEST);
	}

	void EnableMultisample() {
		OpenGL::glEnable(OpenGL::GL_MULTISAMPLE);
	}

	void DisableMultisample() {
		OpenGL::glDisable(OpenGL::GL_MULTISAMPLE);
	}

	int NewProgram(int * shader, int count) {
		int program = OpenGL::glCreateProgram();

		for (int i = 0; i < count; ++i) {
			OpenGL::glAttachShader(program, shader[i]);
		}

		int linked = OpenGL::GL_FALSE;
		OpenGL::glLinkProgram(program);
		OpenGL::glGetProgramiv(program, OpenGL::GL_LINK_STATUS, &linked);

		if (!linked) {
			int logSize = 0;
			OpenGL::glGetProgramInfoLog(program, maxCompilerLog, &logSize, compilerLog);
			compilerLog[logSize] = 0;
			OpenGL::glDeleteProgram(program);
			program = 0;
		} else {
			compilerLog[0] = 0;
			OpenGL::glUseProgram(program);
		} 

		return program;
	}

	void DeleteProgram(int program) {
		int shaders[8] = {};
		int numShaders = 0;

		OpenGL::glGetAttachedShaders(program, 8, &numShaders, (OpenGL::GLuint *)shaders);
		for (int i = 0; i < numShaders; ++i) {
			OpenGL::glDeleteShader(shaders[i]);
		}
		OpenGL::glDeleteProgram(program);
	}

	void UseProgram(int program) {
		OpenGL::glUseProgram(program);
	}

	void UseDefaultProgram() {
		OpenGL::glUseProgram(defaultProgram);
	}

	int NewFragmentShader(const char * source) {
		int shader = OpenGL::glCreateShader(OpenGL::GL_FRAGMENT_SHADER);
		OpenGL::glShaderSource(shader, 1, &source, 0);
		OpenGL::glCompileShader(shader);

		int compiled = OpenGL::GL_FALSE;
		OpenGL::glGetShaderiv(shader, OpenGL::GL_COMPILE_STATUS, &compiled);
		if (!compiled) {
			int logSize = 0;
			OpenGL::glGetShaderInfoLog(shader, maxCompilerLog, &logSize, compilerLog);
			compilerLog[logSize] = 0;
			OpenGL::glDeleteShader(shader);
			shader = 0;
		} else {
			compilerLog[0] = 0;
		}

		return shader;
	}

	int NewGeometryShader(const char * source) {
		int shader = OpenGL::glCreateShader(OpenGL::GL_GEOMETRY_SHADER);
		OpenGL::glShaderSource(shader, 1, &source, 0);
		OpenGL::glCompileShader(shader);

		int compiled = OpenGL::GL_FALSE;
		OpenGL::glGetShaderiv(shader, OpenGL::GL_COMPILE_STATUS, &compiled);
		if (!compiled) {
			int logSize = 0;
			OpenGL::glGetShaderInfoLog(shader, maxCompilerLog, &logSize, compilerLog);
			compilerLog[logSize] = 0;
			OpenGL::glDeleteShader(shader);
			shader = 0;
		} else {
			compilerLog[0] = 0;
		}

		return shader;
	}

	int NewVertexShader(const char * source) {
		int shader = OpenGL::glCreateShader(OpenGL::GL_VERTEX_SHADER);
		OpenGL::glShaderSource(shader, 1, &source, 0);
		OpenGL::glCompileShader(shader);

		int compiled = OpenGL::GL_FALSE;
		OpenGL::glGetShaderiv(shader, OpenGL::GL_COMPILE_STATUS, &compiled);
		if (!compiled) {
			int logSize = 0;
			OpenGL::glGetShaderInfoLog(shader, maxCompilerLog, &logSize, compilerLog);
			compilerLog[logSize] = 0;
			OpenGL::glDeleteShader(shader);
			shader = 0;
		} else {
			compilerLog[0] = 0;
		}

		return shader;
	}

	void DeleteShader(int shader) {
		OpenGL::glDeleteShader(shader);
	}

	const char * CompilerLog() {
		return compilerLog;
	}

	int AttributeLocation(int program, const char * name) {
		return OpenGL::glGetAttribLocation(program, name);
	}

	int UniformLocation(int program, const char * name) {
		return OpenGL::glGetUniformLocation(program, name);
	}

	int UniformBlockLocation(int program, const char * name) {
		return OpenGL::glGetUniformBlockIndex(program, name);
	}

	void Uniform1f(int location, float v0) {
		OpenGL::glUniform1f(location, v0);
	}

	void Uniform2f(int location, float v0, float v1) {
		OpenGL::glUniform2f(location, v0, v1);
	}

	void Uniform3f(int location, float v0, float v1, float v2) {
		OpenGL::glUniform3f(location, v0, v1, v2);
	}

	void Uniform4f(int location, float v0, float v1, float v2, float v3) {
		OpenGL::glUniform4f(location, v0, v1, v2, v3);
	}

	void Uniform1i(int location, int v0) {
		OpenGL::glUniform1i(location, v0);
	}

	void Uniform2i(int location, int v0, int v1) {
		OpenGL::glUniform2i(location, v0, v1);
	}

	void Uniform3i(int location, int v0, int v1, int v2) {
		OpenGL::glUniform3i(location, v0, v1, v2);
	}

	void Uniform4i(int location, int v0, int v1, int v2, int v3) {
		OpenGL::glUniform4i(location, v0, v1, v2, v3);
	}

	void UniformMatrix(int location, const float * matrix) {
		OpenGL::glUniformMatrix4fv(location, 1, false, matrix);
	}

	void UniformTransposeMatrix(int location, const float * matrix) {
		OpenGL::glUniformMatrix4fv(location, 1, true, matrix);
	}

	void UniformBlock(int location, int buffer) {
		OpenGL::glBindBufferBase(OpenGL::GL_UNIFORM_BUFFER, location, buffer);
	}

	int NewTexture(int width, int height, const void * data, int components) {
		if (components < 1 || components > 4) {
			return 0;
		}

		const int formats[] = {0, OpenGL::GL_RED, OpenGL::GL_RG, OpenGL::GL_RGB, OpenGL::GL_RGBA};
		int format = formats[components];

		if (!width && !height) {
			int viewportValue[4];
			OpenGL::glGetIntegerv(OpenGL::GL_VIEWPORT, viewportValue);
			width = viewportValue[2];
			height = viewportValue[3];
		}

		OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + defaultTextureUnit);

		int texture = 0;
		OpenGL::glGenTextures(1, (OpenGL::GLuint *)&texture);
		OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
		OpenGL::glTexImage2D(OpenGL::GL_TEXTURE_2D, 0, format, width, height, 0, format, OpenGL::GL_UNSIGNED_BYTE, data);
		return texture;
	}

	void DeleteTexture(int texture) {
		OpenGL::glDeleteTextures(1, (OpenGL::GLuint *)&texture);
	}

	void UseTexture(int texture, int location) {
		OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + location);
		OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture);
	}

	void UpdateTexture(int texture, int x, int y, int width, int height, const void * data, int components) {
		if (components < 1 || components > 4) {
			return;
		}

		const int formats[] = {0, OpenGL::GL_RED, OpenGL::GL_RG, OpenGL::GL_RGB, OpenGL::GL_RGBA};
		int format = formats[components];
		
		OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + defaultTextureUnit);
		OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture);
		OpenGL::glTexSubImage2D(OpenGL::GL_TEXTURE_2D, 0, x, y, width, height, format, OpenGL::GL_UNSIGNED_BYTE, data);
	}

	void SetTexturePixelated(int texture) {
		OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + defaultTextureUnit);
		OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_NEAREST);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_NEAREST);
	}
	
	void SetTextureFiltered(int texture) {
		OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + defaultTextureUnit);
		OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
	}

	void SetTextureMipmapped(int texture) {
		OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0 + defaultTextureUnit);
		OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR_MIPMAP_LINEAR);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
	}

	void BuildMipmap(int texture, int base, int max) {
		OpenGL::glActiveTexture(OpenGL::GL_TEXTURE0);
		OpenGL::glBindTexture(OpenGL::GL_TEXTURE_2D, texture);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_BASE_LEVEL, base);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAX_LEVEL, max);
		OpenGL::glGenerateMipmap(OpenGL::GL_TEXTURE_2D);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR_MIPMAP_LINEAR);
		OpenGL::glTexParameteri(OpenGL::GL_TEXTURE_2D, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
	}

	int NewVertexArray(const char * format, VertexBufferAndAttribute * attribs, int indexBuffer) {
		// format regex: '([1-4][if])+'

		int length = 0;
		while (format[length]) {
			if (length % 2 == 0) {
				if (format[length] < '1' || format[length] > '4') {
					return 0;
				}
			} else {
				if (format[length] != 'i' && format[length] != 'f') {
					return 0;
				}
			}
			++length;
		}

		if (length % 2) {
			return 0;
		}

		int vertexArray = 0;
		OpenGL::glGenVertexArrays(1, (OpenGL::GLuint *)&vertexArray);

		int stride = 0;
		for (int i = 0; format[i]; i += 2) {
			stride += (format[i] - '0') * 4;
		}

		OpenGL::glBindVertexArray(vertexArray);
		char * ptr = 0;
		for (int i = 0; format[i]; i += 2) {
			int dimension = format[i] - '0';
			int index = attribs[i / 2].attribute;
			OpenGL::glBindBuffer(OpenGL::GL_ARRAY_BUFFER, attribs[i / 2].buffer);
			if (format[i + 1] == 'f') {
				OpenGL::glVertexAttribPointer(index, dimension, OpenGL::GL_FLOAT, false, stride, ptr);
			}
			else
			if (format[i + 1] == 'i') {
				OpenGL::glVertexAttribPointer(index, dimension, OpenGL::GL_INT, false, stride, ptr);
			}
			OpenGL::glEnableVertexAttribArray(index);
			ptr += dimension * 4;
		}
		OpenGL::glBindBuffer(OpenGL::GL_ELEMENT_ARRAY_BUFFER, indexBuffer);
		OpenGL::glBindVertexArray(defaultVertexArray);
		return vertexArray;
	}

	void DeleteVertexArray(int vao) {
		OpenGL::glDeleteVertexArrays(1, (OpenGL::GLuint *)&vao);
	}

	void EnableAttribute(int vao, int target) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glEnableVertexAttribArray(target);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void DisableAttribute(int vao, int target) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDisableVertexAttribArray(target);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void EnableAttributes(int vao, int * target, int count) {
		OpenGL::glBindVertexArray(vao);
		for (int i = 0; i < count; ++i) {
			OpenGL::glEnableVertexAttribArray(target[i]);
		}
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void DisableAttributes(int vao, int * target, int count) {
		OpenGL::glBindVertexArray(vao);
		for (int i = 0; i < count; ++i) {
			OpenGL::glDisableVertexAttribArray(target[i]);
		}
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	int NewVertexBuffer(const void * data, int size) {
		int buffer = 0;
		OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&buffer);
		OpenGL::glBindBuffer(OpenGL::GL_ARRAY_BUFFER, buffer);
		OpenGL::glBufferData(OpenGL::GL_ARRAY_BUFFER, size, data, OpenGL::GL_STATIC_DRAW);
		return buffer;
	}

	int NewIndexBuffer(const void * data, int size) {
		int buffer = 0;
		OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&buffer);
		OpenGL::glBindBuffer(OpenGL::GL_ELEMENT_ARRAY_BUFFER, buffer);
		OpenGL::glBufferData(OpenGL::GL_ELEMENT_ARRAY_BUFFER, size, data, OpenGL::GL_STATIC_DRAW);
		return buffer;
	}

	int NewUniformBuffer(const void * data, int size) {
		int buffer = 0;
		OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&buffer);
		OpenGL::glBindBuffer(OpenGL::GL_UNIFORM_BUFFER, buffer);
		OpenGL::glBufferData(OpenGL::GL_UNIFORM_BUFFER, size, data, OpenGL::GL_STATIC_DRAW);
		return buffer;
	}

	int NewDynamicVertexBuffer(const void * data, int size) {
		int buffer = 0;
		OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&buffer);
		OpenGL::glBindBuffer(OpenGL::GL_ARRAY_BUFFER, buffer);
		OpenGL::glBufferData(OpenGL::GL_ARRAY_BUFFER, size, data, OpenGL::GL_DYNAMIC_DRAW);
		return buffer;
	}

	int NewDynamicIndexBuffer(const void * data, int size) {
		int buffer = 0;
		OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&buffer);
		OpenGL::glBindBuffer(OpenGL::GL_ELEMENT_ARRAY_BUFFER, buffer);
		OpenGL::glBufferData(OpenGL::GL_ELEMENT_ARRAY_BUFFER, size, data, OpenGL::GL_DYNAMIC_DRAW);
		return buffer;
	}

	int NewDynamicUniformBuffer(const void * data, int size) {
		int buffer = 0;
		OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&buffer);
		OpenGL::glBindBuffer(OpenGL::GL_UNIFORM_BUFFER, buffer);
		OpenGL::glBufferData(OpenGL::GL_UNIFORM_BUFFER, size, data, OpenGL::GL_DYNAMIC_DRAW);
		return buffer;
	}

	void DeleteBuffer(int buffer) {
		OpenGL::glDeleteBuffers(1, (OpenGL::GLuint *)&buffer);
	}

	void UpdateVertexBuffer(int buffer, int offset, const void * data, int size) {
		OpenGL::glBindBuffer(OpenGL::GL_ARRAY_BUFFER, buffer);
		OpenGL::glBufferSubData(OpenGL::GL_ARRAY_BUFFER, (OpenGL::GLintptr)offset, size, data);
	}

	void UpdateIndexBuffer(int buffer, int offset, const void * data, int size) {
		OpenGL::glBindBuffer(OpenGL::GL_ELEMENT_ARRAY_BUFFER, buffer);
		OpenGL::glBufferSubData(OpenGL::GL_ELEMENT_ARRAY_BUFFER, (OpenGL::GLintptr)offset, size, data);
	}

	void UpdateUniformBuffer(int buffer, int offset, const void * data, int size) {
		OpenGL::glBindBuffer(OpenGL::GL_UNIFORM_BUFFER, buffer);
		OpenGL::glBufferSubData(OpenGL::GL_UNIFORM_BUFFER, (OpenGL::GLintptr)offset, size, data);
	}

	void RenderTriangles(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDrawArraysInstanced(OpenGL::GL_TRIANGLES, first, count, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderTriangleStrip(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDrawArraysInstanced(OpenGL::GL_TRIANGLE_STRIP, first, count, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderTriangleFan(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDrawArraysInstanced(OpenGL::GL_TRIANGLE_FAN, first, count, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderLines(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDrawArraysInstanced(OpenGL::GL_LINES, first, count, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderLineStrip(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDrawArraysInstanced(OpenGL::GL_LINE_STRIP, first, count, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderLineLoop(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDrawArraysInstanced(OpenGL::GL_LINE_LOOP, first, count, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderPoints(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDrawArraysInstanced(OpenGL::GL_POINTS, first, count, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderLineStripAdjacency(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDrawArraysInstanced(OpenGL::GL_LINE_STRIP_ADJACENCY, first, count, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderLinesAdjacency(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDrawArraysInstanced(OpenGL::GL_LINES_ADJACENCY, first, count, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderTriangleStripAdjacency(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDrawArraysInstanced(OpenGL::GL_TRIANGLE_STRIP_ADJACENCY, first, count, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderTrianglesAdjacency(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		OpenGL::glDrawArraysInstanced(OpenGL::GL_TRIANGLES_ADJACENCY, first, count, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderIndexedTriangles(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElementsInstanced(OpenGL::GL_TRIANGLES, count, OpenGL::GL_UNSIGNED_INT, ptr, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderIndexedTriangleStrip(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElementsInstanced(OpenGL::GL_TRIANGLE_STRIP, count, OpenGL::GL_UNSIGNED_INT, ptr, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderIndexedTriangleFan(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElementsInstanced(OpenGL::GL_TRIANGLE_FAN, count, OpenGL::GL_UNSIGNED_INT, ptr, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderIndexedLines(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElementsInstanced(OpenGL::GL_LINES, count, OpenGL::GL_UNSIGNED_INT, ptr, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderIndexedLineStrip(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElementsInstanced(OpenGL::GL_LINE_STRIP, count, OpenGL::GL_UNSIGNED_INT, ptr, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderIndexedLineLoop(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElementsInstanced(OpenGL::GL_LINE_LOOP, count, OpenGL::GL_UNSIGNED_INT, ptr, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderIndexedPoints(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElementsInstanced(OpenGL::GL_POINTS, count, OpenGL::GL_UNSIGNED_INT, ptr, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderIndexedLineStripAdjacency(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElementsInstanced(OpenGL::GL_LINE_STRIP_ADJACENCY, count, OpenGL::GL_UNSIGNED_INT, ptr, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderIndexedLinesAdjacency(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElementsInstanced(OpenGL::GL_LINES_ADJACENCY, count, OpenGL::GL_UNSIGNED_INT, ptr, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderIndexedTriangleStripAdjacency(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElementsInstanced(OpenGL::GL_TRIANGLE_STRIP_ADJACENCY, count, OpenGL::GL_UNSIGNED_INT, ptr, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	void RenderIndexedTrianglesAdjacency(int vao, int count, int first, int instances) {
		OpenGL::glBindVertexArray(vao);
		const void * ptr = (const void *)((OpenGL::GLintptr)first * 4);
		OpenGL::glDrawElementsInstanced(OpenGL::GL_TRIANGLES_ADJACENCY, count, OpenGL::GL_UNSIGNED_INT, ptr, instances);
		OpenGL::glBindVertexArray(defaultVertexArray);
	}

	Framebuffer NewFramebuffer(int width, int height, bool multisample) {
		int framebuffer = 0;
		int color = 0;
		int depth = 0;

		OpenGL::glGenFramebuffers(1, (OpenGL::GLuint *)&framebuffer);
		OpenGL::glBindFramebuffer(OpenGL::GL_FRAMEBUFFER, framebuffer);

		unsigned target = OpenGL::GL_TEXTURE_2D;
		if (multisample) {
			target = OpenGL::GL_TEXTURE_2D_MULTISAMPLE;
		}

		if (!width && !height) {
			int viewport[4] = {};
			OpenGL::glGetIntegerv(OpenGL::GL_VIEWPORT, viewport);
			width = viewport[2];
			height = viewport[3];
		}

		OpenGL::glGenTextures(1, (OpenGL::GLuint *)&color);
		OpenGL::glBindTexture(target, color);
		OpenGL::glTexParameteri(target, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR);
		OpenGL::glTexParameteri(target, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
		OpenGL::glTexImage2D(target, 0, OpenGL::GL_RGBA, width, height, 0, OpenGL::GL_RGBA, OpenGL::GL_FLOAT, 0);
		OpenGL::glFramebufferTexture2D(OpenGL::GL_FRAMEBUFFER, OpenGL::GL_COLOR_ATTACHMENT0, target, color, 0);

		OpenGL::glGenTextures(1, (OpenGL::GLuint *)&depth);
		OpenGL::glBindTexture(target, depth);
		OpenGL::glTexParameteri(target, OpenGL::GL_TEXTURE_MIN_FILTER, OpenGL::GL_LINEAR);
		OpenGL::glTexParameteri(target, OpenGL::GL_TEXTURE_MAG_FILTER, OpenGL::GL_LINEAR);
		OpenGL::glTexImage2D(target, 0, OpenGL::GL_DEPTH_COMPONENT, width, height, 0, OpenGL::GL_DEPTH_COMPONENT, OpenGL::GL_FLOAT, 0);
		OpenGL::glFramebufferTexture2D(OpenGL::GL_FRAMEBUFFER, OpenGL::GL_DEPTH_ATTACHMENT, target, depth, 0);

		Framebuffer tuple = {
			framebuffer,
			color,
			depth,
		};

		return tuple;

		OpenGL::glBindFramebuffer(OpenGL::GL_FRAMEBUFFER, defaultFramebuffer);
	}

	void DeleteFramebuffer(int framebuffer) {
		int color = 0;
		OpenGL::glGetFramebufferAttachmentParameteriv(OpenGL::GL_FRAMEBUFFER, OpenGL::GL_COLOR_ATTACHMENT0, OpenGL::GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME, (OpenGL::GLint *)&color);

		if (color) {
			OpenGL::glDeleteTextures(1, (OpenGL::GLuint *)&color);
		}

		int depth = 0;
		OpenGL::glGetFramebufferAttachmentParameteriv(OpenGL::GL_FRAMEBUFFER, OpenGL::GL_DEPTH_ATTACHMENT, OpenGL::GL_FRAMEBUFFER_ATTACHMENT_OBJECT_NAME, (OpenGL::GLint *)&depth);

		if (depth) {
			OpenGL::glDeleteTextures(1, (OpenGL::GLuint *)&depth);
		}

		OpenGL::glDeleteFramebuffers(1, (OpenGL::GLuint *)&framebuffer);
	}

	void UseFramebuffer(int framebuffer) {
		OpenGL::glBindFramebuffer(OpenGL::GL_FRAMEBUFFER, framebuffer);
	}

	void UseDefaultFramebuffer() {
		OpenGL::glBindFramebuffer(OpenGL::GL_FRAMEBUFFER, defaultFramebuffer);
	}

	unsigned char * ReadPixels(int x, int y, int width, int height, int components) {
		if (components < 1 || components > 4) {
			return 0;
		}

		const int formats[] = {0, OpenGL::GL_RED, OpenGL::GL_RG, OpenGL::GL_RGB, OpenGL::GL_RGBA};
		int format = formats[components];

		unsigned char * data = (unsigned char *)malloc(width * height * components);
		OpenGL::glReadPixels(x, y, width, height, format, OpenGL::GL_UNSIGNED_BYTE, data);
		return data;
	}

	float * ReadDepthPixels(int x, int y, int width, int height) {
		float * data = (float *)malloc(width * height * sizeof(float));
		OpenGL::glReadPixels(x, y, width, height, OpenGL::GL_DEPTH_COMPONENT, OpenGL::GL_FLOAT, data);
		return data;
	}

	unsigned ReadPixel(int x, int y) {
		unsigned rgba = 0;
		OpenGL::glReadPixels(x, y, 1, 1, OpenGL::GL_RGBA, OpenGL::GL_UNSIGNED_BYTE, &rgba);
		return rgba;
	}

	float ReadDepthPixel(int x, int y) {
		float depth = 0.0;
		OpenGL::glReadPixels(x, y, 1, 1, OpenGL::GL_DEPTH_COMPONENT, OpenGL::GL_FLOAT, &depth);
		return depth;
	}

	// Extension

	bool ExtensionActive() {
		return extensionActive;
	}

	void UseTextureAsImage(int texture, int binding, int components) {
		if (components < 1 || components > 4) {
			return;
		}

		const int formats[] = {0, OpenGL::GL_R8UI, OpenGL::GL_RG8UI, OpenGL::GL_RGB8UI, OpenGL::GL_RGBA8UI};
		int format = formats[components];
		
		OpenGL::glBindImageTexture(binding, texture, 0, false, 0, OpenGL::GL_READ_WRITE, format);
	}

	int NewTessControlShader(const char * source) {
		int shader = OpenGL::glCreateShader(OpenGL::GL_TESS_CONTROL_SHADER);
		OpenGL::glShaderSource(shader, 1, &source, 0);
		OpenGL::glCompileShader(shader);

		int compiled = OpenGL::GL_FALSE;
		OpenGL::glGetShaderiv(shader, OpenGL::GL_COMPILE_STATUS, &compiled);
		if (!compiled) {
			int logSize = 0;
			OpenGL::glGetShaderInfoLog(shader, maxCompilerLog, &logSize, compilerLog);
			compilerLog[logSize] = 0;
			OpenGL::glDeleteShader(shader);
			shader = 0;
		} else {
			compilerLog[0] = 0;
		}

		return shader;
	}

	int NewTessEvaluationShader(const char * source) {
		int shader = OpenGL::glCreateShader(OpenGL::GL_TESS_EVALUATION_SHADER);
		OpenGL::glShaderSource(shader, 1, &source, 0);
		OpenGL::glCompileShader(shader);

		int compiled = OpenGL::GL_FALSE;
		OpenGL::glGetShaderiv(shader, OpenGL::GL_COMPILE_STATUS, &compiled);
		if (!compiled) {
			int logSize = 0;
			OpenGL::glGetShaderInfoLog(shader, maxCompilerLog, &logSize, compilerLog);
			compilerLog[logSize] = 0;
			OpenGL::glDeleteShader(shader);
			shader = 0;
		} else {
			compilerLog[0] = 0;
		}

		return shader;
	}

	int NewComputeShader(const char * source) {
		int shader = OpenGL::glCreateShader(OpenGL::GL_COMPUTE_SHADER);
		OpenGL::glShaderSource(shader, 1, &source, 0);
		OpenGL::glCompileShader(shader);

		int compiled = OpenGL::GL_FALSE;
		OpenGL::glGetShaderiv(shader, OpenGL::GL_COMPILE_STATUS, &compiled);
		if (!compiled) {
			int logSize = 0;
			OpenGL::glGetShaderInfoLog(shader, maxCompilerLog, &logSize, compilerLog);
			compilerLog[logSize] = 0;
			OpenGL::glDeleteShader(shader);
			shader = 0;
		} else {
			compilerLog[0] = 0;
		}

		if (!shader) {
			return 0;
		}

		return NewProgram(&shader, 1);
	}

	void DeleteComputeShader(int program) {
		int shader;
		OpenGL::glGetAttachedShaders(program, 1, 0, (OpenGL::GLuint *)&shader);
		OpenGL::glDeleteShader(shader);
		OpenGL::glDeleteProgram(program);
	}

	void RunComputeShader(int program, int x, int y, int z) {
		OpenGL::glUseProgram(program);
		OpenGL::glDispatchCompute(x, y, z);
	}

	int NewStorageBuffer(const void * data, int size) {
		int buffer = 0;
		OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&buffer);
		OpenGL::glBindBuffer(OpenGL::GL_SHADER_STORAGE_BUFFER, buffer);
		OpenGL::glBufferData(OpenGL::GL_SHADER_STORAGE_BUFFER, size, data, OpenGL::GL_STATIC_DRAW);
		return buffer;
	}

	int NewDynamicStorageBuffer(const void * data, int size) {
		int buffer = 0;
		OpenGL::glGenBuffers(1, (OpenGL::GLuint *)&buffer);
		OpenGL::glBindBuffer(OpenGL::GL_SHADER_STORAGE_BUFFER, buffer);
		OpenGL::glBufferData(OpenGL::GL_SHADER_STORAGE_BUFFER, size, data, OpenGL::GL_DYNAMIC_DRAW);
		return buffer;
	}

	void UpdateStorageBuffer(int buffer, int offset, const void * data, int size) {
		OpenGL::glBindBuffer(OpenGL::GL_SHADER_STORAGE_BUFFER, buffer);
		OpenGL::glBufferSubData(OpenGL::GL_SHADER_STORAGE_BUFFER, (OpenGL::GLintptr)offset, size, data);
	}

	void UseStorageBuffer(int buffer, int binding) {
		OpenGL::glBindBufferBase(OpenGL::GL_SHADER_STORAGE_BUFFER, binding, buffer);
	}

	void * ReadStorageBuffer(int buffer, int offset, int size) {
		OpenGL::glBindBuffer(OpenGL::GL_SHADER_STORAGE_BUFFER, buffer);
		void * map = OpenGL::glMapBufferRange(OpenGL::GL_SHADER_STORAGE_BUFFER, offset, size, OpenGL::GL_MAP_READ_BIT);
		if (!map) {
			return 0;
		}
		void * content = malloc(size);
		if (!content) {
			return 0;
		}
		memcpy(content, map, size);
		OpenGL::glUnmapBuffer(OpenGL::GL_SHADER_STORAGE_BUFFER);
		return content;
	}

	// Better than nothing font
}
