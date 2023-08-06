#pragma once

namespace ModernGL {

	enum EnableEnum {
		ENABLE_NOTHING = 0x00,
		ENABLE_BLEND = 0x01,
		ENABLE_CULL_FACE = 0x02,
		ENABLE_DEPTH_TEST = 0x04,
		ENABLE_MULTISAMPLE = 0x08,
	};

	enum TextureFilterEnum {
		TEXTURE_PIXELATED = 0x01,
		TEXTURE_FILTERED = 0x02,
		TEXTURE_MIPMAPPED = 0x03,
	};

	struct Info {
		int major;
		int minor;
		int samples;
		const char * vendor;
		const char * renderer;
	};

	struct Framebuffer {
		unsigned framebuffer;
		unsigned color;
		unsigned depth;
	};

	extern bool InitializeModernGL(bool font = true);
	extern bool ExtensionActive();
	
	extern const char * GetError();
	extern Info GetInfo();

	extern void Viewport(int x, int y, int w, int h);
	extern void Clear(unsigned char r = 0, unsigned char g = 0, unsigned char b = 0, unsigned char a = 255);

	extern void PointSize(float size);
	extern void LineSize(float size);

	extern void EnableOnly(unsigned mask);
	extern void EnableBlend();
	extern void DisableBlend();
	extern void EnableCullFace();
	extern void DisableCullFace();
	extern void EnableDepthTest();
	extern void DisableDepthTest();
	extern void EnableMultisample();
	extern void DisableMultisample();

	extern unsigned NewProgram(unsigned * shader, int count);
	extern void DeleteProgram(unsigned program);
	extern void UseProgram(unsigned program);
	extern void UseDefaultProgram();

	extern unsigned NewFragmentShader(const char * source);
	extern unsigned NewGeometryShader(const char * source);
	extern unsigned NewVertexShader(const char * source);
	extern unsigned NewComputeShader(const char * source);
	extern unsigned NewTessControlShader(const char * source);
	extern unsigned NewTessEvaluationShader(const char * source);
	extern void DeleteShader(unsigned shader);

	extern const char * CompilerLog();

	extern unsigned AttributeLocation(unsigned program, const char * name);
	extern unsigned UniformLocation(unsigned program, const char * name);
	extern unsigned UniformBlockLocation(unsigned program, const char * name);

	extern void Uniform1f(unsigned location, float v0);
	extern void Uniform2f(unsigned location, float v0, float v1);
	extern void Uniform3f(unsigned location, float v0, float v1, float v2);
	extern void Uniform4f(unsigned location, float v0, float v1, float v2, float v3);
	extern void Uniform1i(unsigned location, int v0);
	extern void Uniform2i(unsigned location, int v0, int v1);
	extern void Uniform3i(unsigned location, int v0, int v1, int v2);
	extern void Uniform4i(unsigned location, int v0, int v1, int v2, int v3);

	extern void UniformMatrix(unsigned location, const float * matrix);
	extern void UniformTransposeMatrix(unsigned location, const float * matrix);
	extern void UniformBlock(unsigned location, unsigned buffer);

	extern unsigned NewTexture(int width, int height, const void * data, int components = 3);
	extern void DeleteTexture(unsigned texture);
	extern void UseTexture(unsigned texture, unsigned location = 0);

	extern void SetTextureFilter(unsigned texture, unsigned mode);
	extern void BuildMipmap(unsigned texture, int base = 0, int max = 1000);

	extern unsigned NewVertexArray(const char * format, int * attribs, unsigned vertexBuffer, unsigned indexBuffer = 0);
	extern void DeleteVertexArray(unsigned array);

	extern void EnableAttribute(unsigned vao, unsigned target);
	extern void DisableAttribute(unsigned vao, unsigned target);
	extern void EnableAttributes(unsigned vao, unsigned * target, int count);
	extern void DisableAttributes(unsigned vao, unsigned * target, int count);

	extern unsigned NewVertexBuffer(const void * data, int size);
	extern unsigned NewIndexBuffer(const void * data, int size);
	extern unsigned NewStorageBuffer(const void * data, int size);
	extern unsigned NewUniformBuffer(const void * data, int size);
	extern unsigned NewDynamicVertexBuffer(const void * data, int size);
	extern unsigned NewDynamicIndexBuffer(const void * data, int size);
	extern unsigned NewDynamicStorageBuffer(const void * data, int size);
	extern unsigned NewDynamicUniformBuffer(const void * data, int size);
	extern void DeleteBuffer(unsigned buffer);

	extern void UpdateVertexBuffer(unsigned buffer, unsigned offset, const void * data, int size);
	extern void UpdateIndexBuffer(unsigned buffer, unsigned offset, const void * data, int size);
	extern void UpdateStorageBuffer(unsigned buffer, unsigned offset, const void * data, int size);
	extern void UpdateUniformBuffer(unsigned buffer, unsigned offset, const void * data, int size);

	extern void UseStorageBuffer(unsigned buffer, unsigned binding);
	extern void * ReadStorageBuffer(unsigned buffer, unsigned offset, int size);

	extern void RenderTriangles(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderTriangleStrip(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderTriangleFan(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderLines(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderLineStrip(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderLineLoop(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderPoints(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderLineStripAdjacency(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderLinesAdjacency(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderTriangleStripAdjacency(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderTrianglesAdjacency(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedTriangles(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedTriangleStrip(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedTriangleFan(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedLines(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedLineStrip(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedLineLoop(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedPoints(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedLineStripAdjacency(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedLinesAdjacency(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedTriangleStripAdjacency(unsigned vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedTrianglesAdjacency(unsigned vao, int count, int first = 0, int instances = 1);

	extern Framebuffer NewFramebuffer(int width, int height, bool multisample = true);
	extern void DeleteFramebuffer(unsigned framebuffer);
	extern void UseFramebuffer(unsigned framebuffer);
	extern void UseDefaultFramebuffer();

	// OpenGL 4.3+
	
	extern unsigned char * ReadPixels(int x, int y, int width, int height, int components = 3);
	extern float * ReadDepthPixels(int x, int y, int width, int height);

	extern unsigned ReadPixel(int x, int y);
	extern float ReadDepthPixel(int x, int y);

	extern unsigned NewTessControlShader(const char * source);
	extern unsigned NewTessEvaluationShader(const char * source);

	extern unsigned NewComputeShader(const char * source);
	extern void DeleteComputeShader(unsigned program);
	extern void RunComputeShader(unsigned program, unsigned x = 1, unsigned y = 1, unsigned z = 1);

	extern unsigned NewStorageBuffer(const void * data, int size);
	extern unsigned NewDynamicStorageBuffer(const void * data, int size);
	extern void UpdateStorageBuffer(unsigned buffer, unsigned offset, const void * data, int size);
	extern void UseStorageBuffer(unsigned buffer, unsigned program, unsigned binding = 0);
	extern void * ReadStorageBuffer(unsigned buffer, unsigned offset, int size);

	// Better than nothing font
}
