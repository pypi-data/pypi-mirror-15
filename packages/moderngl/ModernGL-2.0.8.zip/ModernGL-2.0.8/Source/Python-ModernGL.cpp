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

PyObject * NewDynamicUniformBuffer(PyObject * self, PyObject * args) {
	const void * data;
	int size;

	if (!PyArg_ParseTuple(args, "y#:NewDynamicUniformBuffer", &data, &size)) {
		return 0;
	}

	return PyLong_FromLong(ModernGL::NewDynamicUniformBuffer(data, size));
}

PyObject * DeleteBuffer(PyObject * self, PyObject * args) {
	int buffer;

	if (!PyArg_ParseTuple(args, "i:DeleteBuffer", &buffer)) {
		return 0;
	}

	ModernGL::DeleteBuffer(buffer);
	Py_RETURN_NONE;
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

	if (!PyArg_ParseTuple(args, "|ii:NewFramebuffer", &width, &height)) {
		return 0;
	}

	ModernGL::Framebuffer framebuffer = ModernGL::NewFramebuffer(width, height);
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
	int x = 1;
	int y = 1;
	int z = 1;

	if (!PyArg_ParseTuple(args, "i|iii:RunComputeShader", &program, &x, &y, &z)) {
		return 0;
	}

	ModernGL::RunComputeShader(program, x, y, z);
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
		"Initialize the ModernGL module inside a valid OpenGL context.\n"
		"A valid OpenGL context must exists before the function call.\n"

		"\n"
		"Parameters:\n"
		"\tfont: (bool) Load a better than nothing font. By default is True\n"

		"\n"
		"Returns:\n"
		"\tokey (bool) True on success, False on failure.\n"
		"\n"
	},
	{
		"GetInfo",
		GetInfo,
		METH_VARARGS,
		"Get information about the OpenGL context.\n"

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		// "\tinfo (tuple) Information about the OpenGL context.\n"
		"\tmajor (int) The major OpenGL version.\n"
		"\tminor (int) The minor OpenGL version.\n"
		"\tsamples (int) The samples supported by the default framebuffer.\n"
		"\tvendor (int) The vendor.\n"
		"\trenderer (int) The renderer.\n"
		"\n"
	},
	{
		"GetError",
		GetError,
		METH_VARARGS,
		"Get the error when Initialization failed.\n"

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\terror (str) The reason, why the InitializeModernGL failed.\n"
		"\n"
	},
	{
		"Viewport",
		Viewport,
		METH_VARARGS,
		"Set the viewport for rendering.\n"

		"\n"
		"Parameters:\n"
		"\tx (int) Position of the viewport.\n"
		"\ty (int) Position of the viewport.\n"
		"\twidth (int) Width of the viewport.\n"
		"\theight (int) Height of the viewport.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"Clear",
		Clear,
		METH_VARARGS,
		"Clear the viewport with the specified colors.\n"
		"Also clears the depth attachments.\n"

		"\n"
		"Parameters:\n"
		"\tr (int) Clear value for the red channel. By default is 0\n"
		"\tg (int) Clear value for the green channel. By default is 0\n"
		"\tb (int) Clear value for the blue channel. By default is 0\n"
		"\ta (int) Clear value for the alpha channel. By default is 255\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"PointSize",
		PointSize,
		METH_VARARGS,
		"Set the size of the point primitive.\n"

		"\n"
		"Parameters:\n"
		"\tsize (float) Size of the point.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"LineSize",
		LineSize,
		METH_VARARGS,
		"Set the with of the line primitive.\n"

		"\n"
		"Parameters:\n"
		"\tsize (float) Width of the line.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"EnableOnly",
		EnableOnly,
		METH_VARARGS,
		"Enables only the specified flags.\n"
		"The enable flags are: ENABLE_NOTHING, ENABLE_BLEND, ENABLE_DEPTH_TEST, ENABLE_CULL_FACE and ENABLE_MULTISAMPLE.\n"

		"\n"
		"Parameters:\n"
		"\tflags (int) A combination of the enable flags using bitwise OR operator.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"EnableBlend",
		EnableBlend,
		METH_VARARGS,
		"Enable blending.\n"

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"DisableBlend",
		DisableBlend,
		METH_VARARGS,
		"Disable blending.\n"

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"EnableCullFace",
		EnableCullFace,
		METH_VARARGS,
		"Enable face culling.\n"

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"DisableCullFace",
		DisableCullFace,
		METH_VARARGS,
		"Disable face culling.\n"

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"EnableDepthTest",
		EnableDepthTest,
		METH_VARARGS,
		"Enable depth testing.\n"

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"DisableDepthTest",
		DisableDepthTest,
		METH_VARARGS,
		"Disable depth testing.\n"

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"EnableMultisample",
		EnableMultisample,
		METH_VARARGS,
		"Enable multisampling.\n"

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"DisableMultisample",
		DisableMultisample,
		METH_VARARGS,
		"Disable multisampling.\n"

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"NewVertexShader",
		NewVertexShader,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tsource (str) Source code in GLSL.\n"

		"\n"
		"Returns:\n"
		"\tshader (int) The index of the new shader object.\n"
		"\n"
	},
	{
		"NewFragmentShader",
		NewFragmentShader,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tsource (str) Source code in GLSL.\n"

		"\n"
		"Returns:\n"
		"\tshader (int) The index of the new shader object.\n"
		"\n"
	},
	{
		"NewGeometryShader",
		NewGeometryShader,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tsource (str) Source code in GLSL.\n"

		"\n"
		"Returns:\n"
		"\tshader (int) The index of the new shader object.\n"
		"\n"
	},
	{
		"DeleteShader",
		DeleteShader,
		METH_VARARGS,
		"Delete shader object created by the NewFragmentShader, the NewGeometryShader, the NewTessControlShader, the NewTessEvaluationShader or the NewVertexShader.\n"

		"\n"
		"Parameters:\n"
		"\tshader (int) Index of a shader object.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"NewProgram",
		NewProgram,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tshaders (list of ints) List containing shader indices.\n"

		"\n"
		"Returns:\n"
		"\tprogram (int) The index of the new program object.\n"
		"\n"
	},
	{
		"DeleteProgram",
		DeleteProgram,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tprogram (int) Index of a program object returned by the NewProgram function.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UseProgram",
		UseProgram,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tprogram (int) Index of a program object returned by the NewProgram function.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UseDefaultProgram",
		UseDefaultProgram,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
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
		""

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tlog (str) The GLSL compiler log.\n"
		"\n"
	},
	{
		"AttributeLocation",
		AttributeLocation,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tprogram (int) Index of a program object returned by the NewProgram function.\n"
		"\tname (str) Name of the attribute.\n"

		"\n"
		"Returns:\n"
		"\tlocation (int) The location of the attribute.\n"
		"\n"
	},
	{
		"UniformLocation",
		UniformLocation,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tprogram (int) Index of a program object returned by the NewProgram function.\n"
		"\tname (str) Name of the uniform.\n"

		"\n"
		"Returns:\n"
		"\tlocation (int) The location of the uniform.\n"
		"\n"
	},
	{
		"UniformBlockLocation",
		UniformBlockLocation,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tprogram (int) Index of a program object returned by the NewProgram function.\n"
		"\tname (str) Name of the uniform block.\n"

		"\n"
		"Returns:\n"
		"\tlocation (int) The location of the uniform block.\n"
		"\n"
	},
	{
		"Uniform1f",
		Uniform1f,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `float` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"


		"\n"
		"Parameters:\n"
		"\tlocation (int) Location of the uniform returned by the UniformLocation.\n"
		"\tv0 (float) Value to set.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"Uniform2f",
		Uniform2f,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `vec2` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"


		"\n"
		"Parameters:\n"
		"\tlocation (int) Location of the uniform returned by the UniformLocation.\n"
		"\tv0 (float) Value to set.\n"
		"\tv1 (float) Value to set.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"Uniform3f",
		Uniform3f,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `vec3` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"


		"\n"
		"Parameters:\n"
		"\tlocation (int) Location of the uniform returned by the UniformLocation.\n"
		"\tv0 (float) Value to set.\n"
		"\tv1 (float) Value to set.\n"
		"\tv2 (float) Value to set.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"Uniform4f",
		Uniform4f,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `vec4` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"


		"\n"
		"Parameters:\n"
		"\tlocation (int) Location of the uniform returned by the UniformLocation.\n"
		"\tv0 (float) Value to set.\n"
		"\tv1 (float) Value to set.\n"
		"\tv2 (float) Value to set.\n"
		"\tv3 (float) Value to set.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"Uniform1i",
		Uniform1i,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `int` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"


		"\n"
		"Parameters:\n"
		"\tlocation (int) Location of the uniform returned by the UniformLocation.\n"
		"\tv0 (int) Value to set.\n"


		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"Uniform2i",
		Uniform2i,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `ivec2` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"


		"\n"
		"Parameters:\n"
		"\tlocation (int) Location of the uniform returned by the UniformLocation.\n"
		"\tv0 (int) Value to set.\n"
		"\tv1 (int) Value to set.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"Uniform3i",
		Uniform3i,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `ivec3` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"


		"\n"
		"Parameters:\n"
		"\tlocation (int) Location of the uniform returned by the UniformLocation.\n"
		"\tv0 (int) Value to set.\n"
		"\tv1 (int) Value to set.\n"
		"\tv2 (int) Value to set.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"Uniform4i",
		Uniform4i,
		METH_VARARGS,
		"Set the value of the uniform.\n"
		"The value must have the type of `ivec4` in the shader.\n"
		"The location of the uniform can be queried by the UniformLocation method.\n"


		"\n"
		"Parameters:\n"
		"\tlocation (int) Location of the uniform returned by the UniformLocation.\n"
		"\tv0 (int) Value to set.\n"
		"\tv1 (int) Value to set.\n"
		"\tv2 (int) Value to set.\n"
		"\tv3 (int) Value to set.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UniformMatrix",
		UniformMatrix,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tlocation (int) Location of the uniform returned by the UniformLocation.\n"
		"\tmatrix (list of floats) List containing 4x4=16 float values.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UniformTransposeMatrix",
		UniformTransposeMatrix,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tlocation (int) Location of the uniform returned by the UniformLocation.\n"
		"\tmatrix (list of floats) List containing 4x4=16 float values.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UniformBlock",
		UniformBlock,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tlocation (int) Location of the uniform returned by the UniformLocation.\n"
		"\tubo (int) Index of a uniform buffer returned by a NewUniformBuffer.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"NewTexture",
		NewTexture,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\twidth (int) Width of the texture.\n"
		"\theight (int) Height of the texture.\n"
		"\tpixels (bytes) Pixels stored in bytes.\n"
		"\tcomponents (int) By default is 3\n"

		"\n"
		"Returns:\n"
		"\ttexture (int) The index of the new texture object.\n"
		"\n"
	},
	{
		"DeleteTexture",
		DeleteTexture,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\ttexture (int) Index of a texture returned by the NewTexture function.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UpdateTexture",
		UpdateTexture,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\ttexture (int) Index of a texture returned by the NewTexture function.\n"
		"\tx (int) Offset of the new texture part.\n"
		"\ty (int) Offset of the new texture part.\n"
		"\twidth (int) Width of the texture.\n"
		"\theight (int) Height of the texture.\n"
		"\tpixels (bytes) Pixels stored in bytes.\n"
		"\tcomponents (int) By default is 3\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UseTexture",
		UseTexture,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\ttexture (int) Index of a texture returned by the NewTexture function.\n"
		"\tlocation (int) Location of the texture. By default is 0\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"SetTexturePixelated",
		SetTexturePixelated,
		METH_VARARGS,
		"Set texture filter to nearest.\n"

		"\n"
		"Parameters:\n"
		"\ttexture (int) Index of a texture returned by the NewTexture function.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"SetTextureFiltered",
		SetTextureFiltered,
		METH_VARARGS,
		"Set texture filter to linear.\n"

		"\n"
		"Parameters:\n"
		"\ttexture (int) Index of a texture returned by the NewTexture function.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"SetTextureMipmapped",
		SetTextureMipmapped,
		METH_VARARGS,
		"Set texture filter to mipmap linear.\n"

		"\n"
		"Parameters:\n"
		"\ttexture (int) Index of a texture returned by the NewTexture function.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"BuildMipmap",
		BuildMipmap,
		METH_VARARGS,
		"Generate the mipmaps for the texture.\n"

		"\n"
		"Parameters:\n"
		"\ttexture (int) Index of a texture returned by the NewTexture function.\n"
		"\tbase (int) Base mipmap level to build.\n"
		"\tmax (int) Maximum mipmap level to build.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"NewVertexArray",
		NewVertexArray,
		METH_VARARGS,
		"The foreach int or float attribute an index of a vertex buffer object and the location of a vertex attribute must be specified.\n"

		"\n"
		"Parameters:\n"
		"\tformat (str) Format of the vertex array attrubites. ([1-4][if])+\n"
		"\tattribs (list of int pairs) List of vertex buffer object and vertex location pairs.\n"
		"\tibo (int) Index of an index buffer object. By default is 0\n"

		"\n"
		"Returns:\n"
		"\tvao (int) The index of the new vertex array object.\n"
		"\n"
	},
	{
		"DeleteVertexArray",
		DeleteVertexArray,
		METH_VARARGS,
		""
		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"EnableAttribute",
		EnableAttribute,
		METH_VARARGS,
		"Enable an attribute in the vertex array object.\n"

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object.\n"
		"\tattrib (int) The location of the vertex attribute returned by the AttributeLocation function.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"DisableAttribute",
		DisableAttribute,
		METH_VARARGS,
		"Disable an attribute in the vertex array object.\n"

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object.\n"
		"\tattrib (int) The location of the vertex attribute returned by the AttributeLocation function.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"EnableAttributes",
		EnableAttributes,
		METH_VARARGS,
		"Enable attributes in the vertex array object.\n"

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object.\n"
		"\tattribs (list of ints) The locations of the vertex attributes returned by the AttributeLocation function.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"DisableAttributes",
		DisableAttributes,
		METH_VARARGS,
		"Disable attributes in the vertex array object.\n"

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object.\n"
		"\tattribs (list of ints) The locations of the vertex attributes returned by the AttributeLocation function.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"NewVertexBuffer",
		NewVertexBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"

		"\n"
		"Returns:\n"
		"\tvbo (int) The index of the new vertex buffer object.\n"
		"\n"
	},
	{
		"NewIndexBuffer",
		NewIndexBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"

		"\n"
		"Returns:\n"
		"\tibo (int) The index of the new index buffer object.\n"
		"\n"
	},
	{
		"NewUniformBuffer",
		NewUniformBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"

		"\n"
		"Returns:\n"
		"\tubo (int) The index of the new uniform buffer object.\n"
		"\n"
	},
	{
		"NewDynamicVertexBuffer",
		NewDynamicVertexBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"

		"\n"
		"Returns:\n"
		"\tvbo (int) The index of the new vertex buffer object.\n"
		"\n"
	},
	{
		"NewDynamicIndexBuffer",
		NewDynamicIndexBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"

		"\n"
		"Returns:\n"
		"\tibo (int) The index of the new index buffer object.\n"
		"\n"
	},
	{
		"NewDynamicUniformBuffer",
		NewDynamicUniformBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"

		"\n"
		"Returns:\n"
		"\tubo (int) The index of the new uniform buffer object.\n"
		"\n"
	},
	{
		"DeleteBuffer",
		DeleteBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tbuffer (int) The index of any buffer object except the framebuffer object.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UpdateVertexBuffer",
		UpdateVertexBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tbuffer (int) The index of a vertex buffer object except the framebuffer object.\n"
		"\toffset (int) The offset of the data in the buffer to write.\n"
		"\tdata (bytes) The content of the data to write to the buffer.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UpdateIndexBuffer",
		UpdateIndexBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tbuffer (int) The index of an index buffer object except the framebuffer object.\n"
		"\toffset (int) The offset of the data in the buffer to write.\n"
		"\tdata (bytes) The content of the data to write to the buffer.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UpdateUniformBuffer",
		UpdateUniformBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tbuffer (int) The index of a uniform buffer object except the framebuffer object.\n"
		"\toffset (int) The offset of the data in the buffer to write.\n"
		"\tdata (bytes) The content of the data to write to the buffer.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderTriangles",
		RenderTriangles,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderTriangleStrip",
		RenderTriangleStrip,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderTriangleFan",
		RenderTriangleFan,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderLines",
		RenderLines,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderLineStrip",
		RenderLineStrip,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderLineLoop",
		RenderLineLoop,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderPoints",
		RenderPoints,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderLineStripAdjacency",
		RenderLineStripAdjacency,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderLinesAdjacency",
		RenderLinesAdjacency,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderTriangleStripAdjacency",
		RenderTriangleStripAdjacency,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderTrianglesAdjacency",
		RenderTrianglesAdjacency,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderIndexedTriangles",
		RenderIndexedTriangles,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderIndexedTriangleStrip",
		RenderIndexedTriangleStrip,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderIndexedTriangleFan",
		RenderIndexedTriangleFan,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderIndexedLines",
		RenderIndexedLines,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderIndexedLineStrip",
		RenderIndexedLineStrip,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderIndexedLineLoop",
		RenderIndexedLineLoop,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderIndexedPoints",
		RenderIndexedPoints,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderIndexedLineStripAdjacency",
		RenderIndexedLineStripAdjacency,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderIndexedLinesAdjacency",
		RenderIndexedLinesAdjacency,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderIndexedTriangleStripAdjacency",
		RenderIndexedTriangleStripAdjacency,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RenderIndexedTrianglesAdjacency",
		RenderIndexedTrianglesAdjacency,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tvao (int) The index of a vertex array object that will be used during the rendering.\n"
		"\tcount (int) Number of vertices to render.\n"
		"\tfirst (int) Index of the first vertex. By default is 0\n"
		"\tinstances (int) Number of instances. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"NewFramebuffer",
		NewFramebuffer,
		METH_VARARGS,
		"Creates a framebuffer with two texture attachments. (color and depth)\n"
		"The color attachment have RGBA format, 8bit for each channel.\n"
		"The depth texture contains float values.\n"
		""

		"\n"
		"Parameters:\n"
		"\twidth (int) Width of the framebuffer. By default is 0\n"
		"\theight (int) Height of the framebuffer. By default is 0\n"

		"\n"
		"Returns:\n"
		"\tfbo (int) The index of the new framebuffer object.\n"
		"\tcolor (int) The index of the color attachment texture object.\n"
		"\tdepth (int) The index of the depth attachment texture object.\n"
		"\n"
	},
	{
		"DeleteFramebuffer",
		DeleteFramebuffer,
		METH_VARARGS,

		"\n"
		"Parameters:\n"
		"\tframebuffer (int) Index of the framebuffer returned by the NewFramebuffer.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UseFramebuffer",
		UseFramebuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tframebuffer (int) Index of the framebuffer returned by the NewFramebuffer.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UseDefaultFramebuffer",
		UseDefaultFramebuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	
	{
		"ReadPixels",
		ReadPixels,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tx (int) Offset of the image to read.\n"
		"\ty (int) Offset of the image to read.\n"
		"\twidth (int) Width of the image to read.\n"
		"\theight (int) Height of the image to read.\n"
		"\tcomponents (int) By default is 3\n"

		"\n"
		"Returns:\n"
		"\tpixels (bytes) The color channels selected by components from the active framebuffer.\n"
		"\n"
	},
	{
		"ReadDepthPixels",
		ReadDepthPixels,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tx (int) Offset of the image to read.\n"
		"\ty (int) Offset of the image to read.\n"
		"\twidth (int) Width of the image to read.\n"
		"\theight (int) Height of the image to read.\n"

		"\n"
		"Returns:\n"
		"\tpixels (bytes) The depth channel from the active framebuffer.\n"
		"\n"
	},
	{
		"ReadPixel",
		ReadPixel,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tx (int) Offset of the pixel to read.\n"
		"\ty (int) Offset of the pixel to read.\n"

		"\n"
		"Returns:\n"
		"\tpixels (int) The rgba value at (x, y) from the active framebuffer.\n"
		"\n"
	},
	{
		"ReadDepthPixel",
		ReadDepthPixel,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tx (int) Offset of the pixel to read.\n"
		"\ty (int) Offset of the pixel to read.\n"

		"\n"
		"Returns:\n"
		"\tpixels (float) The depth value at (x, y) from the active framebuffer.\n"
		"\n"
	},

	// Extension

	{
		"ExtensionActive",
		ExtensionActive,
		METH_VARARGS,
		"Check for full ModernGL support.\n"
		"The initialization of the extensions are not affected by this method.\n"

		"\n"
		"Parameters:\n"
		"\tNone\n"

		"\n"
		"Returns:\n"
		"\tactive (bool) True on supported extensions, False otherwise.\n"
		"\n"
	},
	{
		"UseTextureAsImage",
		UseTextureAsImage,
		METH_VARARGS,
		"To use image2D instead of sampler2D.\n"


		"\n"
		"Parameters:\n"
		"\ttexture (int) .\n"
		"\tbinding (int) Image binding specified by the layout in GLSL. By default is 0\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"NewTessEvaluationShader",
		NewTessEvaluationShader,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tsource (str) Source code in GLSL.\n"

		"\n"
		"Returns:\n"
		"\tshader (int) The index of the new shader object.\n"
		"\n"
	},
	{
		"NewTessControlShader",
		NewTessControlShader,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tsource (str) Source code in GLSL.\n"

		"\n"
		"Returns:\n"
		"\tshader (int) The index of the new shader object.\n"
		"\n"
	},
	{
		"NewComputeShader",
		NewComputeShader,
		METH_VARARGS,
		"Compiles and links a compute shader from source.\n"

		"\n"
		"Parameters:\n"
		"\tsource (str) Source code in GLSL.\n"

		"\n"
		"Returns:\n"
		"\tprogram (int) The index of the new program object.\n"
		"\n"
	},
	{
		"DeleteComputeShader",
		DeleteComputeShader,
		METH_VARARGS,
		"Compute shader is a standalone shader program. NOT part of the rendering pipeline.\n"
		"Equivalent to the DeleteProgram.\n"

		"\n"
		"Parameters:\n"
		"\tprogram (int) The index of a program object returned by the NewComputeShader function.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"RunComputeShader",
		RunComputeShader,
		METH_VARARGS,
		"Run the compute shader.\n"

		"\n"
		"Parameters:\n"
		"\tprogram (int) The index of a program object returned by the NewComputeShader function.\n"
		"\tx (int) The x group size of the workers. By default is 1\n"
		"\ty (int) The y group size of the workers. By default is 1\n"
		"\tz (int) The z group size of the workers. By default is 1\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"NewStorageBuffer",
		NewStorageBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"

		"\n"
		"Returns:\n"
		"\tssbo (int) The index of the new shader storage buffer object.\n"
		"\n"
	},
	{
		"NewDynamicStorageBuffer",
		NewDynamicStorageBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tdata (bytes) The content of the buffer.\n"

		"\n"
		"Returns:\n"
		"\tssbo (int) The index of the new shader storage buffer object.\n"
		"\n"
	},
	{
		"UseStorageBuffer",
		UseStorageBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tssbo (int) The index of a shader storage buffer object returned by the NewStorageBuffer.\n"
		"\tbinding (int) Buffer binding specified by the layout in GLSL. By default is 0\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"UpdateStorageBuffer",
		UpdateStorageBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tssbo (int) The index of a shader storage buffer object returned by the NewStorageBuffer.\n"
		"\toffset (int) The offset of the data in the buffer to update.\n"
		"\tdata (bytes) The content of the data to write to the buffer.\n"

		"\n"
		"Returns:\n"
		"\tNone\n"
		"\n"
	},
	{
		"ReadStorageBuffer",
		ReadStorageBuffer,
		METH_VARARGS,
		""

		"\n"
		"Parameters:\n"
		"\tssbo (int) The index of a shader storage buffer object returned by the NewStorageBuffer.\n"
		"\toffset (int) The offset of the data in the buffer to read.\n"
		"\tsize (int) The size of the data to read from the buffer.\n"

		"\n"
		"Returns:\n"
		"\tdata (bytes) The Content of the buffer.\n"
		"\n"
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

	PyModule_AddStringConstant(m, "VERSION", "2.0.8");
	
	PyModule_AddStringConstant(m, "__AUTHOR_NAME__", "Szabolcs Dombi");
	PyModule_AddStringConstant(m, "__AUTHOR_EMAIL__", "cprogrammer1994@gmail.com");

	return m;
}
