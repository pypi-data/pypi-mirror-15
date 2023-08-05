/*
 * Python object definition of the libfwnt security identifier
 *
 * Copyright (C) 2009-2016, Joachim Metz <joachim.metz@gmail.com>
 *
 * Refer to AUTHORS for acknowledgements.
 *
 * This software is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This software is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public License
 * along with this software.  If not, see <http://www.gnu.org/licenses/>.
 */

#include <common.h>
#include <types.h>

#if defined( HAVE_STDLIB_H )
#include <stdlib.h>
#endif

#include "pyfwnt_error.h"
#include "pyfwnt_libcerror.h"
#include "pyfwnt_libcstring.h"
#include "pyfwnt_libfwnt.h"
#include "pyfwnt_python.h"
#include "pyfwnt_security_identifier.h"
#include "pyfwnt_unused.h"

PyMethodDef pyfwnt_security_identifier_object_methods[] = {

	{ "copy_from_byte_stream",
	  (PyCFunction) pyfwnt_security_identifier_copy_from_byte_stream,
	  METH_VARARGS | METH_KEYWORDS,
	  "copy_from_byte_stream(byte_stream)\n"
	  "\n"
	  "Copies the the security identifier from the byte stream." },

	/* Functions to access the security identifier */

	{ "get_string",
	  (PyCFunction) pyfwnt_security_identifier_get_string,
	  METH_NOARGS,
	  "get_string() -> Unicode string or None\n"
	  "\n"
	  "Retrieves the string name." },

	/* Sentinel */
	{ NULL, NULL, 0, NULL }
};

PyGetSetDef pyfwnt_security_identifier_object_get_set_definitions[] = {

	{ "string",
	  (getter) pyfwnt_security_identifier_get_string,
	  (setter) 0,
	  "The string.",
	  NULL },

	/* Sentinel */
	{ NULL, NULL, NULL, NULL, NULL }
};

PyTypeObject pyfwnt_security_identifier_type_object = {
	PyVarObject_HEAD_INIT( NULL, 0 )

	/* tp_name */
	"pyfwnt.security_identifier",
	/* tp_basicsize */
	sizeof( pyfwnt_security_identifier_t ),
	/* tp_itemsize */
	0,
	/* tp_dealloc */
	(destructor) pyfwnt_security_identifier_free,
	/* tp_print */
	0,
	/* tp_getattr */
	0,
	/* tp_setattr */
	0,
	/* tp_compare */
	0,
	/* tp_repr */
	0,
	/* tp_as_number */
	0,
	/* tp_as_sequence */
	0,
	/* tp_as_mapping */
	0,
	/* tp_hash */
	0,
	/* tp_call */
	0,
	/* tp_str */
	0,
	/* tp_getattro */
	0,
	/* tp_setattro */
	0,
	/* tp_as_buffer */
	0,
	/* tp_flags */
	Py_TPFLAGS_DEFAULT,
	/* tp_doc */
	"pyfwnt security identifier object (wraps libfwnt_security_identifier_t)",
	/* tp_traverse */
	0,
	/* tp_clear */
	0,
	/* tp_richcompare */
	0,
	/* tp_weaklistoffset */
	0,
	/* tp_iter */
	0,
	/* tp_iternext */
	0,
	/* tp_methods */
	pyfwnt_security_identifier_object_methods,
	/* tp_members */
	0,
	/* tp_getset */
	pyfwnt_security_identifier_object_get_set_definitions,
	/* tp_base */
	0,
	/* tp_dict */
	0,
	/* tp_descr_get */
	0,
	/* tp_descr_set */
	0,
	/* tp_dictoffset */
	0,
	/* tp_init */
	(initproc) pyfwnt_security_identifier_init,
	/* tp_alloc */
	0,
	/* tp_new */
	0,
	/* tp_free */
	0,
	/* tp_is_gc */
	0,
	/* tp_bases */
	NULL,
	/* tp_mro */
	NULL,
	/* tp_cache */
	NULL,
	/* tp_subclasses */
	NULL,
	/* tp_weaklist */
	NULL,
	/* tp_del */
	0
};

/* Creates a new pyfwnt security identifier object
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyfwnt_security_identifier_new(
           libfwnt_security_identifier_t *security_identifier,
           PyObject *parent_object )
{
	pyfwnt_security_identifier_t *pyfwnt_security_identifier = NULL;
	static char *function                                    = "pyfwnt_security_identifier_new";

	if( security_identifier == NULL )
	{
		PyErr_Format(
		 PyExc_TypeError,
		 "%s: invalid security identifier.",
		 function );

		return( NULL );
	}
	pyfwnt_security_identifier = PyObject_New(
	                              struct pyfwnt_security_identifier,
	                              &pyfwnt_security_identifier_type_object );

	if( pyfwnt_security_identifier == NULL )
	{
		PyErr_Format(
		 PyExc_MemoryError,
		 "%s: unable to initialize security identifier.",
		 function );

		goto on_error;
	}
	if( pyfwnt_security_identifier_init(
	     pyfwnt_security_identifier ) != 0 )
	{
		PyErr_Format(
		 PyExc_MemoryError,
		 "%s: unable to initialize security identifier.",
		 function );

		goto on_error;
	}
	pyfwnt_security_identifier->security_identifier = security_identifier;
	pyfwnt_security_identifier->parent_object       = parent_object;

	if( pyfwnt_security_identifier->parent_object != NULL )
	{
		Py_IncRef(
		 pyfwnt_security_identifier->parent_object );
	}
	return( (PyObject *) pyfwnt_security_identifier );

on_error:
	if( pyfwnt_security_identifier != NULL )
	{
		Py_DecRef(
		 (PyObject *) pyfwnt_security_identifier );
	}
	return( NULL );
}

/* Intializes a security identifier object
 * Returns 0 if successful or -1 on error
 */
int pyfwnt_security_identifier_init(
     pyfwnt_security_identifier_t *pyfwnt_security_identifier )
{
	static char *function = "pyfwnt_security_identifier_init";

	if( pyfwnt_security_identifier == NULL )
	{
		PyErr_Format(
		 PyExc_TypeError,
		 "%s: invalid security identifier.",
		 function );

		return( -1 );
	}
	/* Make sure libfwnt security identifier is set to NULL
	 */
	pyfwnt_security_identifier->security_identifier = NULL;

	return( 0 );
}

/* Frees a security identifier object
 */
void pyfwnt_security_identifier_free(
      pyfwnt_security_identifier_t *pyfwnt_security_identifier )
{
	libcerror_error_t *error    = NULL;
	struct _typeobject *ob_type = NULL;
	static char *function       = "pyfwnt_security_identifier_free";
	int result                  = 0;

	if( pyfwnt_security_identifier == NULL )
	{
		PyErr_Format(
		 PyExc_TypeError,
		 "%s: invalid security identifier.",
		 function );

		return;
	}
	if( pyfwnt_security_identifier->security_identifier == NULL )
	{
		PyErr_Format(
		 PyExc_TypeError,
		 "%s: invalid security identifier - missing libfwnt security identifier.",
		 function );

		return;
	}
	ob_type = Py_TYPE(
	           pyfwnt_security_identifier );

	if( ob_type == NULL )
	{
		PyErr_Format(
		 PyExc_ValueError,
		 "%s: missing ob_type.",
		 function );

		return;
	}
	if( ob_type->tp_free == NULL )
	{
		PyErr_Format(
		 PyExc_ValueError,
		 "%s: invalid ob_type - missing tp_free.",
		 function );

		return;
	}
	Py_BEGIN_ALLOW_THREADS

	result = libfwnt_security_identifier_free(
	          &( pyfwnt_security_identifier->security_identifier ),
	          &error );

	Py_END_ALLOW_THREADS

	if( result != 1 )
	{
		pyfwnt_error_raise(
		 error,
		 PyExc_MemoryError,
		 "%s: unable to free security identifier.",
		 function );

		libcerror_error_free(
		 &error );
	}
	if( pyfwnt_security_identifier->parent_object != NULL )
	{
		Py_DecRef(
		 pyfwnt_security_identifier->parent_object );
	}
	ob_type->tp_free(
	 (PyObject*) pyfwnt_security_identifier );
}

/* Copies the security identifier from a byte stream
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyfwnt_security_identifier_copy_from_byte_stream(
           pyfwnt_security_identifier_t *pyfwnt_security_identifier,
           PyObject *arguments,
           PyObject *keywords )
{
	PyObject *string_object     = NULL;
	libcerror_error_t *error    = NULL;
	static char *function       = "pyfwnt_security_identifier_copy_from_byte_stream";
	static char *keyword_list[] = { "byte_stream", NULL };
	const char *byte_stream     = NULL;
	Py_ssize_t byte_stream_size = 0;
	int result                  = 0;

	if( pyfwnt_security_identifier == NULL )
	{
		PyErr_Format(
		 PyExc_TypeError,
		 "%s: invalid security identifier.",
		 function );

		return( NULL );
	}
	if( PyArg_ParseTupleAndKeywords(
	     arguments,
	     keywords,
	     "O",
	     keyword_list,
	     &string_object ) == 0 )
	{
		return( NULL );
	}
	PyErr_Clear();

#if PY_MAJOR_VERSION >= 3
	result = PyObject_IsInstance(
		  string_object,
		  (PyObject *) &PyBytes_Type );
#else
	result = PyObject_IsInstance(
		  string_object,
		  (PyObject *) &PyString_Type );
#endif
	if( result == -1 )
	{
		pyfwnt_error_fetch_and_raise(
	         PyExc_RuntimeError,
		 "%s: unable to determine if string object is of type string.",
		 function );

		return( NULL );
	}
	else if( result == 0 )
	{
		PyErr_Format(
		 PyExc_TypeError,
		 "%s: unsupported string object type",
		 function );

		return( NULL );
	}
	PyErr_Clear();

#if PY_MAJOR_VERSION >= 3
	byte_stream = PyBytes_AsString(
	               string_object );

	byte_stream_size = PyBytes_Size(
	                    string_object );
#else
	byte_stream = PyString_AsString(
	               string_object );

	byte_stream_size = PyString_Size(
	                    string_object );
#endif
/* TODO size bounds check */

	Py_BEGIN_ALLOW_THREADS

	result = libfwnt_security_identifier_copy_from_byte_stream(
	          pyfwnt_security_identifier->security_identifier,
	          (uint8_t *) byte_stream,
	          (size_t) byte_stream_size,
	          LIBFWNT_ENDIAN_LITTLE,
	          &error );

	Py_END_ALLOW_THREADS

	if( result != 1 )
	{
		pyfwnt_error_raise(
		 error,
		 PyExc_IOError,
		 "%s: unable to copy security identifier from byte stream.",
		 function );

		libcerror_error_free(
		 &error );

		return( NULL );
	}
	Py_IncRef(
	 Py_None );

	return( Py_None );
}

/* Retrieves the string
 * Returns a Python object if successful or NULL on error
 */
PyObject *pyfwnt_security_identifier_get_string(
           pyfwnt_security_identifier_t *pyfwnt_security_identifier,
           PyObject *arguments PYFWNT_ATTRIBUTE_UNUSED )
{
	libcerror_error_t *error     = NULL;
	PyObject *string_object      = NULL;
	const char *errors           = NULL;
	uint8_t *string              = NULL;
	static char *function        = "pyfwnt_security_identifier_get_string";
	size_t string_size           = 0;
	uint32_t string_format_flags = 0;
	int result                   = 0;

	PYFWNT_UNREFERENCED_PARAMETER( arguments )

	if( pyfwnt_security_identifier == NULL )
	{
		PyErr_Format(
		 PyExc_TypeError,
		 "%s: invalid security identifier.",
		 function );

		return( NULL );
	}
	Py_BEGIN_ALLOW_THREADS

	result = libfwnt_security_identifier_get_string_size(
	          pyfwnt_security_identifier->security_identifier,
	          &string_size,
	          string_format_flags,
	          &error );

	Py_END_ALLOW_THREADS

	if( result == -1 )
	{
		pyfwnt_error_raise(
		 error,
		 PyExc_IOError,
		 "%s: unable to retrieve string size.",
		 function );

		libcerror_error_free(
		 &error );

		goto on_error;
	}
	else if( ( result == 0 )
	      || ( string_size == 0 ) )
	{
		Py_IncRef(
		 Py_None );

		return( Py_None );
	}
	string = (uint8_t *) PyMem_Malloc(
	                      sizeof( uint8_t ) * string_size );

	if( string == NULL )
	{
		PyErr_Format(
		 PyExc_IOError,
		 "%s: unable to create string.",
		 function );

		goto on_error;
	}
	Py_BEGIN_ALLOW_THREADS

	result = libfwnt_security_identifier_copy_to_utf8_string(
		  pyfwnt_security_identifier->security_identifier,
		  string,
		  string_size,
		  string_format_flags,
		  &error );

	Py_END_ALLOW_THREADS

	if( result != 1 )
	{
		pyfwnt_error_raise(
		 error,
		 PyExc_IOError,
		 "%s: unable to retrieve string.",
		 function );

		libcerror_error_free(
		 &error );

		goto on_error;
	}
	/* Pass the string length to PyUnicode_DecodeUTF8
	 * otherwise it makes the end of string character is part
	 * of the string
	 */
	string_object = PyUnicode_DecodeUTF8(
			 (char *) string,
			 (Py_ssize_t) string_size - 1,
			 errors );

	PyMem_Free(
	 string );

	return( string_object );

on_error:
	if( string != NULL )
	{
		PyMem_Free(
		 string );
	}
	return( NULL );
}

