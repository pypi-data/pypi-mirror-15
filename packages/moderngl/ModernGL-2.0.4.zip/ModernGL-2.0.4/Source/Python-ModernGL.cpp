#include "Python.h"

#include "ModernGL.hpp"

PyObject * InitializeModernGL(PyObject * self, PyObject * args) {
	bool font = true;
	if (!PyArg_ParseTuple(args, "|p:InitializeModernGL", &font)) {
		return 0;
	}
	
	if (ModernGL::InitializeModernGL(font)) {
		Py_RETURN_TRUE;
	} else {
		Py_RETURN_FALSE;
	}
}

PyObject * GetInfo(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":GetInfo")) {
		return 0;
	}

	ModernGL::Info info = ModernGL::GetInfo();
	return Py_BuildValue("iiiss", info.major, info.minor, info.samples, info.vendor, info.renderer);
}

PyObject * GetError(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":GetError")) {
		return 0;
	}

	return PyUnicode_FromString(ModernGL::GetError());
}

PyObject * Viewport(PyObject * self, PyObject * args) {
	int x;
	int y;
	int w;
	int h;

	if (!PyArg_ParseTuple(args, "iiii:Viewport", &x, &y, &w, &h)) {
		return 0;
	}

	ModernGL::Viewport(x, y, w, h);
	Py_RETURN_NONE;
}

PyObject * Clear(PyObject * self, PyObject * args) {
	unsigned char r = 0;
	unsigned char g = 0;
	unsigned char b = 0;
	unsigned char a = 255;

	if (!PyArg_ParseTuple(args, "|bbbb:Clear", &r, &g, &b, &a)) {
		return 0;
	}

	ModernGL::Clear(r, g, b, a);
	Py_RETURN_NONE;
}

PyObject * PointSize(PyObject * self, PyObject * args) {
	float size;

	if (!PyArg_ParseTuple(args, "f:PointSize", &size)) {
		return 0;
	}

	ModernGL::PointSize(size);
	Py_RETURN_NONE;
}

PyObject * LineSize(PyObject * self, PyObject * args) {
	float size;

	if (!PyArg_ParseTuple(args, "f:LineSize", &size)) {
		return 0;
	}

	ModernGL::LineSize(size);
	Py_RETURN_NONE;
}

PyObject * EnableOnly(PyObject * self, PyObject * args) {
	unsigned mask;

	if (!PyArg_ParseTuple(args, "I:EnableOnly", &mask)) {
		return 0;
	}

	ModernGL::EnableOnly(mask);
	Py_RETURN_NONE;
}

PyObject * EnableBlend(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":EnableBlend")) {
		return 0;
	}

	ModernGL::EnableBlend();
	Py_RETURN_NONE;
}

PyObject * DisableBlend(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":DisableBlend")) {
		return 0;
	}

	ModernGL::DisableBlend();
	Py_RETURN_NONE;
}

PyObject * EnableCullFace(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":EnableCullFace")) {
		return 0;
	}

	ModernGL::EnableCullFace();
	Py_RETURN_NONE;
}

PyObject * DisableCullFace(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":DisableCullFace")) {
		return 0;
	}

	ModernGL::DisableCullFace();
	Py_RETURN_NONE;
}

PyObject * EnableDepthTest(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":EnableDepthTest")) {
		return 0;
	}

	ModernGL::EnableDepthTest();
	Py_RETURN_NONE;
}

PyObject * DisableDepthTest(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":DisableDepthTest")) {
		return 0;
	}

	ModernGL::DisableDepthTest();
	Py_RETURN_NONE;
}

PyObject * EnableMultisample(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":EnableMultisample")) {
		return 0;
	}

	ModernGL::EnableMultisample();
	Py_RETURN_NONE;
}

PyObject * DisableMultisample(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":DisableMultisample")) {
		return 0;
	}

	ModernGL::DisableMultisample();
	Py_RETURN_NONE;
}

PyObject * NewFragmentShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewFragmentShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewFragmentShader(source));
}

PyObject * NewGeometryShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewGeometryShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewGeometryShader(source));
}

PyObject * NewVertexShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewVertexShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewVertexShader(source));
}

PyObject * DeleteShader(PyObject * self, PyObject * args) {
	int shader;

	if (!PyArg_ParseTuple(args, "i:DeleteShader", &shader)) {
		return 0;
	}

	ModernGL::DeleteShader(shader);
	Py_RETURN_NONE;
}

PyObject * NewProgram(PyObject * self, PyObject * args) {
	PyObject * lst;

	if (!PyArg_ParseTuple(args, "O:NewProgram", &lst)) {
		return 0;
	}

	int count = PyList_Size(lst);
	int * shader = new int[count];
	for (int i = 0; i < count; ++i) {
		shader[i] = PyLong_AsLong(PyList_GetItem(lst, i));
	}
	int program = ModernGL::NewProgram(shader, count);
	delete[] shader;

	return PyLong_FromLong(program);
}

PyObject * DeleteProgram(PyObject * self, PyObject * args) {
	int program;

	if (!PyArg_ParseTuple(args, "i:DeleteProgram", &program)) {
		return 0;
	}

	ModernGL::DeleteProgram(program);
	Py_RETURN_NONE;
}

PyObject * UseProgram(PyObject * self, PyObject * args) {
	int program;

	if (!PyArg_ParseTuple(args, "i:UseProgram", &program)) {
		return 0;
	}

	ModernGL::UseProgram(program);
	Py_RETURN_NONE;
}

PyObject * UseDefaultProgram(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":UseDefaultProgram")) {
		return 0;
	}

	ModernGL::UseDefaultProgram();
	Py_RETURN_NONE;
}

PyObject * CompilerLog(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":CompilerLog")) {
		return 0;
	}

	return PyUnicode_FromString(ModernGL::CompilerLog());
}

PyObject * AttributeLocation(PyObject * self, PyObject * args) {
	int program;
	const char * name;

	if (!PyArg_ParseTuple(args, "is:AttributeLocation", &program, &name)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::AttributeLocation(program, name));
}

PyObject * UniformLocation(PyObject * self, PyObject * args) {
	int program;
	const char * name;

	if (!PyArg_ParseTuple(args, "is:UniformLocation", &program, &name)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::UniformLocation(program, name));
}

PyObject * UniformBlockLocation(PyObject * self, PyObject * args) {
	int program;
	const char * name;

	if (!PyArg_ParseTuple(args, "is:UniformBlockLocation", &program, &name)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::UniformBlockLocation(program, name));
}

PyObject * Uniform1f(PyObject * self, PyObject * args) {
	int location;
	float v0;

	if (!PyArg_ParseTuple(args, "if:Uniform1f", &location, &v0)) {
		return 0;
	}

	ModernGL::Uniform1f(location, v0);
	Py_RETURN_NONE;
}

PyObject * Uniform2f(PyObject * self, PyObject * args) {
	int location;
	float v0;
	float v1;

	if (!PyArg_ParseTuple(args, "iff:Uniform2f", &location, &v0, &v1)) {
		return 0;
	}

	ModernGL::Uniform2f(location, v0, v1);
	Py_RETURN_NONE;
}

PyObject * Uniform3f(PyObject * self, PyObject * args) {
	int location;
	float v0;
	float v1;
	float v2;

	if (!PyArg_ParseTuple(args, "ifff:Uniform3f", &location, &v0, &v1, &v2)) {
		return 0;
	}

	ModernGL::Uniform3f(location, v0, v1, v2);
	Py_RETURN_NONE;
}

PyObject * Uniform4f(PyObject * self, PyObject * args) {
	int location;
	float v0;
	float v1;
	float v2;
	float v3;

	if (!PyArg_ParseTuple(args, "iffff:Uniform4f", &location, &v0, &v1, &v2, &v3)) {
		return 0;
	}

	ModernGL::Uniform4f(location, v0, v1, v2, v3);
	Py_RETURN_NONE;
}

PyObject * Uniform1i(PyObject * self, PyObject * args) {
	int location;
	int v0;

	if (!PyArg_ParseTuple(args, "ii:Uniform1i", &location, &v0)) {
		return 0;
	}

	ModernGL::Uniform1i(location, v0);
	Py_RETURN_NONE;
}

PyObject * Uniform2i(PyObject * self, PyObject * args) {
	int location;
	int v0;
	int v1;

	if (!PyArg_ParseTuple(args, "iii:Uniform2i", &location, &v0, &v1)) {
		return 0;
	}

	ModernGL::Uniform2i(location, v0, v1);
	Py_RETURN_NONE;
}

PyObject * Uniform3i(PyObject * self, PyObject * args) {
	int location;
	int v0;
	int v1;
	int v2;

	if (!PyArg_ParseTuple(args, "iiii:Uniform3i", &location, &v0, &v1, &v2)) {
		return 0;
	}

	ModernGL::Uniform3i(location, v0, v1, v2);
	Py_RETURN_NONE;
}

PyObject * Uniform4i(PyObject * self, PyObject * args) {
	int location;
	int v0;
	int v1;
	int v2;
	int v3;

	if (!PyArg_ParseTuple(args, "iiiii:Uniform4i", &location, &v0, &v1, &v2, &v3)) {
		return 0;
	}

	ModernGL::Uniform4i(location, v0, v1, v2, v3);
	Py_RETURN_NONE;
}

PyObject * UniformMatrix(PyObject * self, PyObject * args) {
	int location;
	PyObject * lst;

	if (!PyArg_ParseTuple(args, "iO:UniformMatrix", &location, &lst)) {
		return 0;
	}

	float matrix[16];

	int count = PyList_Size(lst);
	for (int i = 0; i < count; ++i) {
		matrix[i] = (float)PyFloat_AsDouble(PyList_GetItem(lst, i));
	}

	ModernGL::UniformMatrix(location, matrix);
	Py_RETURN_NONE;
}

PyObject * UniformTransposeMatrix(PyObject * self, PyObject * args) {
	int location;
	PyObject * lst;

	if (!PyArg_ParseTuple(args, "iO:UniformTransposeMatrix", &location, &lst)) {
		return 0;
	}

	float matrix[16];

	int count = PyList_Size(lst);
	for (int i = 0; i < count; ++i) {
		matrix[i] = (float)PyFloat_AsDouble(PyList_GetItem(lst, i));
	}

	ModernGL::UniformTransposeMatrix(location, matrix);
	Py_RETURN_NONE;
}

PyObject * UniformBlock(PyObject * self, PyObject * args) {
	int location;
	int buffer;

	if (!PyArg_ParseTuple(args, "ii:UniformBlock", &location, &buffer)) {
		return 0;
	}

	ModernGL::UniformBlock(location, buffer);
	Py_RETURN_NONE;
}

PyObject * NewTexture(PyObject * self, PyObject * args) {
	int width;
	int height;
	const void * data;
	int components = 3;
	int size;

	if (!PyArg_ParseTuple(args, "iiy#|i:NewTexture", &width, &height, &data, &size, &components)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewTexture(width, height, data, components));
}

PyObject * DeleteTexture(PyObject * self, PyObject * args) {
	int texture;

	if (!PyArg_ParseTuple(args, "i:DeleteTexture", &texture)) {
		return 0;
	}

	ModernGL::DeleteTexture(texture);
	Py_RETURN_NONE;
}

PyObject * UpdateTexture(PyObject * self, PyObject * args) {
	int texture;
	int x;
	int y;
	int width;
	int height;
	const void * data;
	int components = 3;
	int size;

	if (!PyArg_ParseTuple(args, "iiiiiy#|i:UpdateTexture", &texture, &x, &y, &width, &height, &data, &size, &components)) {
		return 0;
	}

	ModernGL::UpdateTexture(texture, x, y, width, height, data, components);
	Py_RETURN_NONE;
}

PyObject * UseTexture(PyObject * self, PyObject * args) {
	int texture;
	int location = 0;

	if (!PyArg_ParseTuple(args, "i|i:UseTexture", &texture, &location)) {
		return 0;
	}

	ModernGL::UseTexture(texture, location);
	Py_RETURN_NONE;
}

PyObject * SetTexturePixelated(PyObject * self, PyObject * args) {
	int texture;
	
	if (!PyArg_ParseTuple(args, "i:SetTexturePixelated", &texture)) {
		return 0;
	}

	ModernGL::SetTexturePixelated(texture);
	Py_RETURN_NONE;
}

PyObject * SetTextureFiltered(PyObject * self, PyObject * args) {
	int texture;
	
	if (!PyArg_ParseTuple(args, "i:SetTextureFiltered", &texture)) {
		return 0;
	}

	ModernGL::SetTextureFiltered(texture);
	Py_RETURN_NONE;
}

PyObject * SetTextureMipmapped(PyObject * self, PyObject * args) {
	int texture;
	
	if (!PyArg_ParseTuple(args, "i:SetTextureMipmapped", &texture)) {
		return 0;
	}

	ModernGL::SetTextureMipmapped(texture);
	Py_RETURN_NONE;
}

PyObject * BuildMipmap(PyObject * self, PyObject * args) {
	int texture;
	int base = 0;
	int max = 1000;

	if (!PyArg_ParseTuple(args, "i|ii:BuildMipmap", &texture, &base, &max)) {
		return 0;
	}

	ModernGL::BuildMipmap(texture, base, max);
	Py_RETURN_NONE;
}

PyObject * NewVertexArray(PyObject * self, PyObject * args) {
	const char * format;
	PyObject * lst;

	int indexBuffer = 0;

	if (!PyArg_ParseTuple(args, "sO|i:NewVertexArray", &format, &lst, &indexBuffer)) {
		return 0;
	}

	int count = PyList_Size(lst);
	ModernGL::VertexBufferAndAttribute * attribs = new ModernGL::VertexBufferAndAttribute[count];
	for (int i = 0; i < count; ++i) {
		PyObject * tuple = PyList_GetItem(lst, i);
		attribs[i] = {
			PyLong_AsLong(PyTuple_GetItem(tuple, 0)),
			PyLong_AsLong(PyTuple_GetItem(tuple, 1)),
		};
	}

	PyObject * result = PyLong_FromLong(ModernGL::NewVertexArray(format, attribs, indexBuffer));
	delete[] attribs;
	return result;
}

PyObject * DeleteVertexArray(PyObject * self, PyObject * args) {
	int vao;

	if (!PyArg_ParseTuple(args, "i:DeleteVertexArray", &vao)) {
		return 0;
	}

	ModernGL::DeleteVertexArray(vao);
	Py_RETURN_NONE;
}

PyObject * EnableAttribute(PyObject * self, PyObject * args) {
	int vao;
	int target;

	if (!PyArg_ParseTuple(args, "ii:EnableAttribute", &vao, &target)) {
		return 0;
	}

	ModernGL::EnableAttribute(vao, target);
	Py_RETURN_NONE;
}

PyObject * DisableAttribute(PyObject * self, PyObject * args) {
	int vao;
	int target;

	if (!PyArg_ParseTuple(args, "ii:DisableAttribute", &vao, &target)) {
		return 0;
	}

	ModernGL::DisableAttribute(vao, target);
	Py_RETURN_NONE;
}

PyObject * EnableAttributes(PyObject * self, PyObject * args) {
	int vao;
	PyObject * attribs;

	if (!PyArg_ParseTuple(args, "iO:EnableAttributes", &vao, &attribs)) {
		return 0;
	}

	int size = PyList_Size(attribs);
	int * attrib_array = new int[size];
	for (int i = 0; i < size; ++i) {
		attrib_array[i] = PyLong_AsLong(PyList_GetItem(attribs, i));
	}
	ModernGL::EnableAttributes(vao, attrib_array, size);
	delete[] attrib_array;
	Py_RETURN_NONE;
}

PyObject * DisableAttributes(PyObject * self, PyObject * args) {
	int vao;
	PyObject * attribs;

	if (!PyArg_ParseTuple(args, "iO:DisableAttributes", &vao, &attribs)) {
		return 0;
	}

	int size = PyList_Size(attribs);
	int * attrib_array = new int[size];
	for (int i = 0; i < size; ++i) {
		attrib_array[i] = PyLong_AsLong(PyList_GetItem(attribs, i));
	}
	ModernGL::DisableAttributes(vao, attrib_array, size);
	delete[] attrib_array;
	Py_RETURN_NONE;
}

PyObject * NewVertexBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewVertexBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewVertexBuffer(data, size));
}

PyObject * NewIndexBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewIndexBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewIndexBuffer(data, size));
}

PyObject * NewUniformBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewUniformBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewUniformBuffer(data, size));
}

PyObject * NewDynamicVertexBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewDynamicVertexBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewDynamicVertexBuffer(data, size));
}

PyObject * NewDynamicIndexBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewDynamicIndexBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewDynamicIndexBuffer(data, size));
}

PyObject * DeleteBuffer(PyObject * self, PyObject * args) {
	int buffer;

	if (!PyArg_ParseTuple(args, "i:DeleteBuffer", &buffer)) {
		return 0;
	}

	ModernGL::DeleteBuffer(buffer);
	Py_RETURN_NONE;
}

PyObject * NewDynamicUniformBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewDynamicUniformBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewDynamicUniformBuffer(data, size));
}

PyObject * UpdateVertexBuffer(PyObject * self, PyObject * args) {
	int buffer;
	int offset;
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "iiy#:UpdateVertexBuffer", &buffer, &offset, &data, &size)) {
		return 0;
	}

	ModernGL::UpdateVertexBuffer(buffer, offset, data, size);
	Py_RETURN_NONE;
}

PyObject * UpdateIndexBuffer(PyObject * self, PyObject * args) {
	int buffer;
	int offset;
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "iiy#:UpdateIndexBuffer", &buffer, &offset, &data, &size)) {
		return 0;
	}

	ModernGL::UpdateIndexBuffer(buffer, offset, data, size);
	Py_RETURN_NONE;
}

PyObject * UpdateUniformBuffer(PyObject * self, PyObject * args) {
	int buffer;
	int offset;
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "iiy#:UpdateUniformBuffer", &buffer, &offset, &data, &size)) {
		return 0;
	}

	ModernGL::UpdateUniformBuffer(buffer, offset, data, size);
	Py_RETURN_NONE;
}

PyObject * RenderTriangles(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderTriangles", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderTriangles(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderTriangleStrip(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderTriangleStrip", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderTriangleStrip(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderTriangleFan(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderTriangleFan", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderTriangleFan(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderLines(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderLines", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderLines(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderLineStrip(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderLineStrip", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderLineStrip(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderLineLoop(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderLineLoop", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderLineLoop(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderPoints(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderPoints", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderPoints(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderLineStripAdjacency(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderLineStripAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderLineStripAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderLinesAdjacency(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderLinesAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderLinesAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderTriangleStripAdjacency(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderTriangleStripAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderTriangleStripAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderTrianglesAdjacency(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderTrianglesAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderTrianglesAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedTriangles(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderIndexedTriangles", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedTriangles(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedTriangleStrip(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderIndexedTriangleStrip", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedTriangleStrip(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedTriangleFan(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderIndexedTriangleFan", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedTriangleFan(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedLines(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderIndexedLines", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedLines(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedLineStrip(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderIndexedLineStrip", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedLineStrip(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedLineLoop(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderIndexedLineLoop", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedLineLoop(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedPoints(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderIndexedPoints", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedPoints(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedLineStripAdjacency(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderIndexedLineStripAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedLineStripAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedLinesAdjacency(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderIndexedLinesAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedLinesAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedTriangleStripAdjacency(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderIndexedTriangleStripAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedTriangleStripAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * RenderIndexedTrianglesAdjacency(PyObject * self, PyObject * args) {
	int vao;
	int count;
	int first = 0;
	int instances = 1;

	if (!PyArg_ParseTuple(args, "ii|ii:RenderIndexedTrianglesAdjacency", &vao, &count, &first, &instances)) {
		return 0;
	}

	ModernGL::RenderIndexedTrianglesAdjacency(vao, count, first, instances);
	Py_RETURN_NONE;
}

PyObject * NewFramebuffer(PyObject * self, PyObject * args) {
	int width = 0;
	int height = 0;
	bool multisample = true;

	if (!PyArg_ParseTuple(args, "|iip:NewFramebuffer", &width, &height, &multisample)) {
		return 0;
	}

	ModernGL::Framebuffer framebuffer = ModernGL::NewFramebuffer(width, height, multisample);
	return Py_BuildValue("iii", framebuffer.framebuffer, framebuffer.color, framebuffer.depth);
}

PyObject * DeleteFramebuffer(PyObject * self, PyObject * args) {
	int framebuffer;

	if (!PyArg_ParseTuple(args, "i:DeleteFramebuffer", &framebuffer)) {
		return 0;
	}

	ModernGL::DeleteFramebuffer(framebuffer);
	Py_RETURN_NONE;
}

PyObject * UseFramebuffer(PyObject * self, PyObject * args) {
	int framebuffer;

	if (!PyArg_ParseTuple(args, "i:UseFramebuffer", &framebuffer)) {
		return 0;
	}

	ModernGL::UseFramebuffer(framebuffer);
	Py_RETURN_NONE;
}

PyObject * UseDefaultFramebuffer(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":UseDefaultFramebuffer")) {
		return 0;
	}

	ModernGL::UseDefaultFramebuffer();
	Py_RETURN_NONE;
}

PyObject * ReadPixels(PyObject * self, PyObject * args) {
	int x;
	int y;
	int width;
	int height;
	int components = 3;

	if (!PyArg_ParseTuple(args, "iiii|i:ReadPixels", &x, &y, &width, &height, &components)) {
		return 0;
	}

	int size = height * ((width * components + 3) & ~3);
	unsigned char * pixels = ModernGL::ReadPixels(x, y, width, height, components);
	PyObject * data = PyBytes_FromStringAndSize((const char *)pixels, size);
	free(pixels);

	return data;
}

PyObject * ReadDepthPixels(PyObject * self, PyObject * args) {
	int x;
	int y;
	int width;
	int height;

	if (!PyArg_ParseTuple(args, "iiii:ReadDepthPixels", &x, &y, &width, &height)) {
		return 0;
	}

	int size = height * height * 4;
	float * pixels = ModernGL::ReadDepthPixels(x, y, width, height);
	PyObject * data = PyBytes_FromStringAndSize((const char *)pixels, size);
	free(pixels);

	return data;
}

PyObject * ReadPixel(PyObject * self, PyObject * args) {
	int x;
	int y;

	if (!PyArg_ParseTuple(args, "ii:ReadPixel", &x, &y)) {
		return 0;
	}

	return PyLong_FromUnsignedLong(ModernGL::ReadPixel(x, y));
}

PyObject * ReadDepthPixel(PyObject * self, PyObject * args) {
	int x;
	int y;

	if (!PyArg_ParseTuple(args, "ii:ReadDepthPixel", &x, &y)) {
		return 0;
	}

	return PyFloat_FromDouble(ModernGL::ReadDepthPixel(x, y));
}

// Extension

PyObject * ExtensionActive(PyObject * self, PyObject * args) {
	if (!PyArg_ParseTuple(args, ":ExtensionActive")) {
		return 0;
	}

	if (ModernGL::ExtensionActive()) {
		Py_RETURN_TRUE;
	} else {
		Py_RETURN_FALSE;
	}
}

PyObject * UseTextureAsImage(PyObject * self, PyObject * args) {
	int texture;
	int binding = 0;
	int components = 3;

	if (!PyArg_ParseTuple(args, "i|ii:UseTextureAsImage", &texture, &binding, &components)) {
		return 0;
	}

	ModernGL::UseTextureAsImage(texture, binding, components);
	Py_RETURN_NONE;
}

PyObject * NewTessEvaluationShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewTessEvaluationShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewTessEvaluationShader(source));
}

PyObject * NewTessControlShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewTessControlShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewTessControlShader(source));
}

PyObject * NewComputeShader(PyObject * self, PyObject * args) {
	const char * source;

	if (!PyArg_ParseTuple(args, "s:NewComputeShader", &source)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewComputeShader(source));
}

PyObject * DeleteComputeShader(PyObject * self, PyObject * args) {
	int program;

	if (!PyArg_ParseTuple(args, "i:DeleteComputeShader", &program)) {
		return 0;
	}

	ModernGL::DeleteComputeShader(program);
	Py_RETURN_NONE;
}

PyObject * RunComputeShader(PyObject * self, PyObject * args) {
	int program;

	if (!PyArg_ParseTuple(args, "i:RunComputeShader", &program)) {
		return 0;
	}

	ModernGL::RunComputeShader(program);
	Py_RETURN_NONE;
}

PyObject * NewStorageBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewStorageBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewStorageBuffer(data, size));
}

PyObject * NewDynamicStorageBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewDynamicStorageBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewDynamicStorageBuffer(data, size));
}

PyObject * UpdateStorageBuffer(PyObject * self, PyObject * args) {
	int buffer;
	int offset;
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "iiy#:UpdateStorageBuffer", &buffer, &offset, &data, &size)) {
		return 0;
	}

	ModernGL::UpdateStorageBuffer(buffer, offset, data, size);
	Py_RETURN_NONE;
}

PyObject * UseStorageBuffer(PyObject * self, PyObject * args) {
	int buffer;
	int binding = 0;

	if (!PyArg_ParseTuple(args, "i|i:UseStorageBuffer", &buffer, &binding)) {
		return 0;
	}

	ModernGL::UseStorageBuffer(buffer, binding);
	Py_RETURN_NONE;
}

PyObject * ReadStorageBuffer(PyObject * self, PyObject * args) {
	int buffer;
	int offset;
	int size;

	if (!PyArg_ParseTuple(args, "iii:ReadStorageBuffer", &buffer, &offset, &size)) {
		return 0;
	}

	void * content = ModernGL::ReadStorageBuffer(buffer, offset, size);
	if (!content) {
		return 0;
	}
	
	PyObject * data = PyBytes_FromStringAndSize((const char *)content, size);
	free(content);

	return data;
}

static PyMethodDef methods[] = {
	{
		"InitializeModernGL",
		InitializeModernGL,
		METH_VARARGS,
		"Initialize the ModernGL module inside a valid OpenGL context."
	},
	{
		"GetInfo",
		GetInfo,
		METH_VARARGS,
		"Get information about the OpenGL context."
	},
	{
		"GetError",
		GetError,
		METH_VARARGS,
		"Get the error when Initialization failed."
	},

	{
		"Viewport",
		Viewport,
		METH_VARARGS,
		"Set the viewport for rendering.\n"
		"Parameters: (x, y, width, height)"
	},
	{
		"Clear",
		Clear,
		METH_VARARGS,
		"Clear the viewport with the specified colors.\n"
		"Parameters: (r = 0, g = 0, b = 0, a = 255)."
	},

	{
		"PointSize",
		PointSize,
		METH_VARARGS,
		"Set the size of the point primitive."
	},
	{
		"LineSize",
		LineSize,
		METH_VARARGS,
		"Set the with of the line primitive."
	},

	{
		"EnableOnly",
		EnableOnly,
		METH_VARARGS,
		""
	},
	{
		"EnableBlend",
		EnableBlend,
		METH_VARARGS,
		"Enable blending."
	},
	{
		"DisableBlend",
		DisableBlend,
		METH_VARARGS,
		"Disable blending."
	},
	{
		"EnableCullFace",
		EnableCullFace,
		METH_VARARGS,
		"Enable face culling."
	},
	{
		"DisableCullFace",
		DisableCullFace,
		METH_VARARGS,
		"Disable face culling."
	},
	{
		"EnableDepthTest",
		EnableDepthTest,
		METH_VARARGS,
		"Enable depth testing."
	},
	{
		"DisableDepthTest",
		DisableDepthTest,
		METH_VARARGS,
		"Disable depth testing."
	},
	{
		"EnableMultisample",
		EnableMultisample,
		METH_VARARGS,
		"Enable multisampling."
	},
	{
		"DisableMultisample",
		DisableMultisample,
		METH_VARARGS,
		"Disable multisampling."
	},

	{
		"NewFragmentShader",
		NewFragmentShader,
		METH_VARARGS,
		""
	},
	{
		"NewGeometryShader",
		NewGeometryShader,
		METH_VARARGS,
		""
	},
	{
		"NewVertexShader",
		NewVertexShader,
		METH_VARARGS,
		""
	},
	{
		"DeleteShader",
		DeleteShader,
		METH_VARARGS,
		""
	},

	{
		"NewProgram",
		NewProgram,
		METH_VARARGS,
		""
	},
	{
		"DeleteProgram",
		DeleteProgram,
		METH_VARARGS,
		""
	},
	{
		"UseProgram",
		UseProgram,
		METH_VARARGS,
		""
	},
	{
		"UseDefaultProgram",
		UseDefaultProgram,
		METH_VARARGS,
		""
	},

	{
		"CompilerLog",
		CompilerLog,
		METH_VARARGS,
		"Get the compiler log for the following methods:\n"
		"NewFragmentShader\n"
		"NewGeometryShader\n"
		"NewVertexShader\n"
		"NewProgram\n"
		"NewTessEvaluationShader\n"
		"NewTessControlShader\n"
		"NewComputeShader\n"
	},

	{
		"AttributeLocation",
		AttributeLocation,
		METH_VARARGS,
		""
	},
	{
		"UniformLocation",
		UniformLocation,
		METH_VARARGS,
		""
	},
	{
		"UniformBlockLocation",
		UniformBlockLocation,
		METH_VARARGS,
		""
	},

	{
		"Uniform1f",
		Uniform1f,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `vec1` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"
		"Parameters: (location, v0)\n"
	},
	{
		"Uniform2f",
		Uniform2f,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `vec2` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"
		"Parameters: (location, v0, v1)\n"
	},
	{
		"Uniform3f",
		Uniform3f,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `vec3` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"
		"Parameters: (location, v0, v1, v2)\n"
	},
	{
		"Uniform4f",
		Uniform4f,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `vec4` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"
		"Parameters: (location, v0, v1, v2, v3).\n"
	},
	{
		"Uniform1i",
		Uniform1i,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `ivec1` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"
		"Parameters: (location, v0)\n"
	},
	{
		"Uniform2i",
		Uniform2i,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `ivec2` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"
		"Parameters: (location, v0, v1)\n"
	},
	{
		"Uniform3i",
		Uniform3i,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `ivec3` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"
		"Parameters: (location, v0, v1, v2)\n"
	},
	{
		"Uniform4i",
		Uniform4i,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `ivec4` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"
		"Parameters: (location, v0, v1, v2, v3)\n"
	},

	{
		"UniformMatrix",
		UniformMatrix,
		METH_VARARGS,
		""
	},
	{
		"UniformTransposeMatrix",
		UniformTransposeMatrix,
		METH_VARARGS,
		""
	},
	{
		"UniformBlock",
		UniformBlock,
		METH_VARARGS,
		""
	},

	{
		"NewTexture",
		NewTexture,
		METH_VARARGS,
		""
	},
	{
		"DeleteTexture",
		DeleteTexture,
		METH_VARARGS,
		""
	},

	{
		"UpdateTexture",
		UpdateTexture,
		METH_VARARGS,
		""
	},
	{
		"UseTexture",
		UseTexture,
		METH_VARARGS,
		""
	},

	{
		"SetTexturePixelated",
		SetTexturePixelated,
		METH_VARARGS,
		"Set texture filter to nearest."
	},
	{
		"SetTextureFiltered",
		SetTextureFiltered,
		METH_VARARGS,
		"Set texture filter to linear."
	},
	{
		"SetTextureMipmapped",
		SetTextureMipmapped,
		METH_VARARGS,
		"Set texture filter to mipmap linear."
	},
	{
		"BuildMipmap",
		BuildMipmap,
		METH_VARARGS,
		"Build the mipmaps for a texture."
	},

	{
		"NewVertexArray",
		NewVertexArray,
		METH_VARARGS,
		""
	},
	{
		"DeleteVertexArray",
		DeleteVertexArray,
		METH_VARARGS,
		""
	},

	{
		"EnableAttribute",
		EnableAttribute,
		METH_VARARGS,
		"Enable an attribute in the vertex array object."
	},
	{
		"DisableAttribute",
		DisableAttribute,
		METH_VARARGS,
		"Disable an attribute in the vertex array object."
	},
	{
		"EnableAttributes",
		EnableAttributes,
		METH_VARARGS,
		"Enable attributes in the vertex array object."
	},
	{
		"DisableAttributes",
		DisableAttributes,
		METH_VARARGS,
		"Disable attributes in the vertex array object."
	},

	{
		"NewVertexBuffer",
		NewVertexBuffer,
		METH_VARARGS,
		""
	},
	{
		"NewIndexBuffer",
		NewIndexBuffer,
		METH_VARARGS,
		""
	},
	{
		"NewUniformBuffer",
		NewUniformBuffer,
		METH_VARARGS,
		""
	},

	{
		"NewDynamicVertexBuffer",
		NewDynamicVertexBuffer,
		METH_VARARGS,
		""
	},
	{
		"NewDynamicIndexBuffer",
		NewDynamicIndexBuffer,
		METH_VARARGS,
		""
	},
	{
		"NewDynamicUniformBuffer",
		NewDynamicUniformBuffer,
		METH_VARARGS,
		""
	},

	{
		"DeleteBuffer",
		DeleteBuffer,
		METH_VARARGS,
		""
	},

	{
		"UpdateVertexBuffer",
		UpdateVertexBuffer,
		METH_VARARGS,
		""
	},
	{
		"UpdateIndexBuffer",
		UpdateIndexBuffer,
		METH_VARARGS,
		""
	},
	{
		"UpdateUniformBuffer",
		UpdateUniformBuffer,
		METH_VARARGS,
		""
	},

	{
		"RenderTriangles",
		RenderTriangles,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderTriangleStrip",
		RenderTriangleStrip,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderTriangleFan",
		RenderTriangleFan,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderLines",
		RenderLines,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderLineStrip",
		RenderLineStrip,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderLineLoop",
		RenderLineLoop,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderPoints",
		RenderPoints,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderLineStripAdjacency",
		RenderLineStripAdjacency,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderLinesAdjacency",
		RenderLinesAdjacency,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderTriangleStripAdjacency",
		RenderTriangleStripAdjacency,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderTrianglesAdjacency",
		RenderTrianglesAdjacency,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderIndexedTriangles",
		RenderIndexedTriangles,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderIndexedTriangleStrip",
		RenderIndexedTriangleStrip,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderIndexedTriangleFan",
		RenderIndexedTriangleFan,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderIndexedLines",
		RenderIndexedLines,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderIndexedLineStrip",
		RenderIndexedLineStrip,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderIndexedLineLoop",
		RenderIndexedLineLoop,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderIndexedPoints",
		RenderIndexedPoints,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderIndexedLineStripAdjacency",
		RenderIndexedLineStripAdjacency,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderIndexedLinesAdjacency",
		RenderIndexedLinesAdjacency,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderIndexedTriangleStripAdjacency",
		RenderIndexedTriangleStripAdjacency,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},
	{
		"RenderIndexedTrianglesAdjacency",
		RenderIndexedTrianglesAdjacency,
		METH_VARARGS,
		"Parameters: (vao, count, first = 0, instances = 1)."
	},

	{
		"NewFramebuffer",
		NewFramebuffer,
		METH_VARARGS,
		"Creates a framebuffer with two texture attachments. (color and depth)\n"
		"The color attachment have RGBA format, 8bit for each channel\n."
		"The depth texture contains float values.\n"
		"Return value: (framebuffer, color, depth).\n"
		"Parameters: (width, height, multisample = True)\n."
	},
	{
		"DeleteFramebuffer",
		DeleteFramebuffer,
		METH_VARARGS,
		""
	},
	{
		"UseFramebuffer",
		UseFramebuffer,
		METH_VARARGS,
		""
	},
	{
		"UseDefaultFramebuffer",
		UseDefaultFramebuffer,
		METH_VARARGS,
		""
	},
	
	{
		"ReadPixels",
		ReadPixels,
		METH_VARARGS,
		""
	},
	{
		"ReadDepthPixels",
		ReadDepthPixels,
		METH_VARARGS,
		""
	},
	{
		"ReadPixel",
		ReadPixel,
		METH_VARARGS,
		""
	},
	{
		"ReadDepthPixel",
		ReadDepthPixel,
		METH_VARARGS,
		""
	},

	// Extension

	{
		"ExtensionActive",
		ExtensionActive,
		METH_VARARGS,
		"Check for full ModernGL support.\n"
		"The initialization of the extensions are not affected by this method.\n"
	},

	{
		"UseTextureAsImage",
		UseTextureAsImage,
		METH_VARARGS,
		"To use image2D instead of sampler2D."
	},
	
	{
		"NewTessEvaluationShader",
		NewTessEvaluationShader,
		METH_VARARGS,
		""
	},
	{
		"NewTessControlShader",
		NewTessControlShader,
		METH_VARARGS,
		""
	},

	{
		"NewComputeShader",
		NewComputeShader,
		METH_VARARGS,
		"Compiles and links a compute shader from source."
	},
	{
		"DeleteComputeShader",
		DeleteComputeShader,
		METH_VARARGS,
		"Compute shader is a standalone shader program. NOT part of the rendering pipeline.\n"
		"Equivalent to the DeleteProgram.\n"
	},
	{
		"RunComputeShader",
		RunComputeShader,
		METH_VARARGS,
		"Run the compute shader.\n"
		"Parameters: (x = 1, y = 1, z = 1)\n"
	},

	{
		"NewStorageBuffer",
		NewStorageBuffer,
		METH_VARARGS,
		""
	},
	{
		"NewDynamicStorageBuffer",
		NewDynamicStorageBuffer,
		METH_VARARGS,
		""
	},
	{
		"UseStorageBuffer",
		UseStorageBuffer,
		METH_VARARGS,
		""
	},
	{
		"UpdateStorageBuffer",
		UpdateStorageBuffer,
		METH_VARARGS,
		""
	},
	{
		"ReadStorageBuffer",
		ReadStorageBuffer,
		METH_VARARGS,
		""
	},

	// Better than nothing font

	// {"DebugFontColor", DebugFontColor, METH_VARARGS, 0},
	// {"DebugFontAlight", DebugFontAlight, METH_VARARGS, 0},
	// {"DebugFontPrint", DebugFontPrint, METH_VARARGS, 0},

	{0, 0},
};

static struct PyModuleDef moduledef = {PyModuleDef_HEAD_INIT, "ModernGL", 0, -1, methods, 0, 0, 0, 0};

extern "C" {
	PyObject * PyInit_ModernGL();
}

PyObject * PyInit_ModernGL() {
	PyObject * m = PyModule_Create(&moduledef);

	PyModule_AddIntConstant(m, "ENABLE_NOTHING", 0x00);
	PyModule_AddIntConstant(m, "ENABLE_BLEND", 0x01);
	PyModule_AddIntConstant(m, "ENABLE_CULL_FACE", 0x02);
	PyModule_AddIntConstant(m, "ENABLE_DEPTH_TEST", 0x04);
	PyModule_AddIntConstant(m, "ENABLE_MULTISAMPLE", 0x08);

	PyModule_AddStringConstant(m, "VERSION", "2.0.4");
	
	PyModule_AddStringConstant(m, "__AUTHOR_NAME__", "Szabolcs Dombi");
	PyModule_AddStringConstant(m, "__AUTHOR_EMAIL__", "cprogrammer1994@gmail.com");

	return m;
}
