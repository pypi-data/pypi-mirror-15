#pragma once

namespace ModernGL {

	enum EnableEnum {
		ENABLE_NOTHING = 0x00,
		ENABLE_BLEND = 0x01,
		ENABLE_CULL_FACE = 0x02,
		ENABLE_DEPTH_TEST = 0x04,
		ENABLE_MULTISAMPLE = 0x08,
	};

	struct Info {
		int major;
		int minor;
		int samples;
		const char * vendor;
		const char * renderer;
	};

	struct Framebuffer {
		int framebuffer;
		int color;
		int depth;
	};

	struct VertexBufferAndAttribute {
		int buffer;
		int attribute;
	};

	extern bool InitializeModernGL(bool font = true);
	
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

	extern int NewProgram(int * shader, int count);
	extern void DeleteProgram(int program);
	extern void UseProgram(int program);
	extern void UseDefaultProgram();

	extern int NewFragmentShader(const char * source);
	extern int NewGeometryShader(const char * source);
	extern int NewVertexShader(const char * source);
	extern void DeleteShader(int shader);

	extern const char * CompilerLog();

	extern int AttributeLocation(int program, const char * name);
	extern int UniformLocation(int program, const char * name);
	extern int UniformBlockLocation(int program, const char * name);

	extern void Uniform1f(int location, float v0);
	extern void Uniform2f(int location, float v0, float v1);
	extern void Uniform3f(int location, float v0, float v1, float v2);
	extern void Uniform4f(int location, float v0, float v1, float v2, float v3);
	extern void Uniform1i(int location, int v0);
	extern void Uniform2i(int location, int v0, int v1);
	extern void Uniform3i(int location, int v0, int v1, int v2);
	extern void Uniform4i(int location, int v0, int v1, int v2, int v3);

	extern void UniformMatrix(int location, const float * matrix);
	extern void UniformTransposeMatrix(int location, const float * matrix);
	extern void UniformBlock(int location, int buffer);

	extern int NewTexture(int width, int height, const void * data, int components = 3);
	extern void DeleteTexture(int texture);

	extern void UpdateTexture(int texture, int x, int y, int width, int height, const void * data, int components = 3);
	extern void UseTexture(int texture, int location = 0);

	extern void SetTexturePixelated(int texture);
	extern void SetTextureFiltered(int texture);
	extern void SetTextureMipmapped(int texture);
	extern void BuildMipmap(int texture, int base = 0, int max = 1000);

	extern int NewVertexArray(const char * format, VertexBufferAndAttribute * attribs, int indexBuffer = 0);
	extern void DeleteVertexArray(int vao);

	extern void EnableAttribute(int vao, int target);
	extern void DisableAttribute(int vao, int target);
	extern void EnableAttributes(int vao, int * target, int count);
	extern void DisableAttributes(int vao, int * target, int count);

	extern int NewVertexBuffer(const void * data, int size);
	extern int NewIndexBuffer(const void * data, int size);
	extern int NewUniformBuffer(const void * data, int size);
	extern int NewDynamicVertexBuffer(const void * data, int size);
	extern int NewDynamicIndexBuffer(const void * data, int size);
	extern int NewDynamicUniformBuffer(const void * data, int size);
	extern void DeleteBuffer(int buffer);

	extern void UpdateVertexBuffer(int buffer, int offset, const void * data, int size);
	extern void UpdateIndexBuffer(int buffer, int offset, const void * data, int size);
	extern void UpdateUniformBuffer(int buffer, int offset, const void * data, int size);

	extern void RenderTriangles(int vao, int count, int first = 0, int instances = 1);
	extern void RenderTriangleStrip(int vao, int count, int first = 0, int instances = 1);
	extern void RenderTriangleFan(int vao, int count, int first = 0, int instances = 1);
	extern void RenderLines(int vao, int count, int first = 0, int instances = 1);
	extern void RenderLineStrip(int vao, int count, int first = 0, int instances = 1);
	extern void RenderLineLoop(int vao, int count, int first = 0, int instances = 1);
	extern void RenderPoints(int vao, int count, int first = 0, int instances = 1);
	extern void RenderLineStripAdjacency(int vao, int count, int first = 0, int instances = 1);
	extern void RenderLinesAdjacency(int vao, int count, int first = 0, int instances = 1);
	extern void RenderTriangleStripAdjacency(int vao, int count, int first = 0, int instances = 1);
	extern void RenderTrianglesAdjacency(int vao, int count, int first = 0, int instances = 1);

	extern void RenderIndexedTriangles(int vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedTriangleStrip(int vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedTriangleFan(int vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedLines(int vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedLineStrip(int vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedLineLoop(int vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedPoints(int vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedLineStripAdjacency(int vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedLinesAdjacency(int vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedTriangleStripAdjacency(int vao, int count, int first = 0, int instances = 1);
	extern void RenderIndexedTrianglesAdjacency(int vao, int count, int first = 0, int instances = 1);

	extern Framebuffer NewFramebuffer(int width, int height, bool multisample = true);
	extern void DeleteFramebuffer(int framebuffer);
	extern void UseFramebuffer(int framebuffer);
	extern void UseDefaultFramebuffer();
	
	extern unsigned char * ReadPixels(int x, int y, int width, int height, int components = 3);
	extern float * ReadDepthPixels(int x, int y, int width, int height);
	
	extern unsigned ReadPixel(int x, int y);
	extern float ReadDepthPixel(int x, int y);

	// Extensions
	
	extern bool ExtensionActive();

	extern void UseTextureAsImage(int texture, int binding = 0, int components = 3);
	
	extern int NewTessControlShader(const char * source);
	extern int NewTessEvaluationShader(const char * source);

	extern int NewComputeShader(const char * source);
	extern void DeleteComputeShader(int program);
	extern void RunComputeShader(int program, int x = 1, int y = 1, int z = 1);

	extern int NewStorageBuffer(const void * data, int size);
	extern int NewDynamicStorageBuffer(const void * data, int size);
	extern void UpdateStorageBuffer(int buffer, int offset, const void * data, int size);
	extern void UseStorageBuffer(int buffer, int binding = 0);
	extern void * ReadStorageBuffer(int buffer, int offset, int size);

	// Better than nothing font
	// soon

}
