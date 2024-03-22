import base64
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql.cursors
import hashlib
import boto3
import dotenv

# Configuración de la conexión a la base de datos
def get_db_connection():
    return pymysql.connect(host=os.getenv('DB_HOST'),
                           user=os.getenv('DB_USER'),
                           password=os.getenv('DB_PASSWORD'),
                           database=os.getenv('DB_SCHEMA'),
                           cursorclass=pymysql.cursors.DictCursor)

# Función para generar MD5
def generate_md5(data):
    return hashlib.md5(data.encode()).hexdigest()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
dotenv.load_dotenv()

s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('S3_PUBLIC_ACCESS'),
    aws_secret_access_key=os.getenv('S3_SECRET_ACCESS'),
    region_name='us-east-1'
)

# Rutas
@app.route('/check', methods=['GET'])
def check():
    return '', 200

@app.route('/api/usuarios/registro', methods=['POST'])
def registro_usuario():
    data = request.json
    usuario, nombre_completo, contrasena, photo_url = data['usuario'], data['nombre_completo'], generate_md5(data['contrasena']), data['photo_url']
    query = "INSERT INTO usuarios (usuario, nombre_completo, contrasena, foto_perfil_url) VALUES (%s, %s, %s, %s)"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (usuario, nombre_completo, contrasena, photo_url))
            conn.commit()
    except Exception as e:
        print(e)
        return 'Error al registrar usuario', 500
    finally:
        conn.close()

    return 'Usuario registrado', 201

@app.route('/api/usuarios/login', methods=['POST'])
def login_usuario():
    data = request.json
    usuario, contrasena = data['usuario'], generate_md5(data['contrasena'])
    query = "SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (usuario, contrasena))
            result = cursor.fetchone()
            if not result:
                return 'Usuario o contraseña incorrectos', 401
    except Exception as e:
        print(e)
        return 'Error al iniciar sesión', 500
    finally:
        conn.close()

    return 'Usuario logueado', 200

@app.route('/api/usuarios/perfil/<usuario>', methods=['GET'])
def get_perfil_usuario(usuario):
    query = "SELECT usuario, nombre_completo, foto_perfil_url FROM usuarios WHERE usuario = %s"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (usuario,))
            result = cursor.fetchone()
            if not result:
                return 'Usuario no encontrado', 401
    except Exception as e:
        print(e)
        return 'Error al obtener perfil de usuario', 500
    finally:
        conn.close()

    return jsonify(result), 200

@app.route('/api/usuarios/perfil/<usuario>', methods=['PUT'])
def put_perfil_usuario(usuario):
    data = request.json
    nuevo_usuario, nombre_completo, foto_perfil_url, contrasena = data.get('nuevo_usuario', usuario), data['nombre_completo'], data['foto_perfil_url'], generate_md5(data['contrasena'])
    queryVerificacion = "SELECT contrasena FROM usuarios WHERE usuario = %s"
    queryActualizacion = "UPDATE usuarios SET usuario = %s, nombre_completo = %s, foto_perfil_url = %s WHERE usuario = %s"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(queryVerificacion, (usuario,))
            result = cursor.fetchone()
            if not result or result['contrasena'] != contrasena:
                return 'Contraseña incorrecta o usuario no encontrado', 401
            
            cursor.execute(queryActualizacion, (nuevo_usuario, nombre_completo, foto_perfil_url, usuario))
            conn.commit()
    except Exception as e:
        print(e)
        return 'Error al actualizar perfil de usuario', 500
    finally:
        conn.close()

    return 'Perfil de usuario actualizado correctamente', 200


@app.route('/api/fotos', methods=['POST'])
def create_photo():
    data = request.json
    nombre_foto, album, foto_base64, username = data['nombre_foto'], data['album'], data['foto_base64'], data['username']
   
    # Step 1: Find the user_id
    queryFindUser = 'SELECT usuario_id FROM usuarios WHERE usuario = %s'
    # Step 2: find the album_id
    queryFindAlbum = 'SELECT album_id FROM albumes WHERE nombre = %s AND usuario_id = %s'
    # Step 3: Insert the photo
    queryInsertPhoto = 'INSERT INTO fotos (nombre, url, album_id, usuario_id) VALUES (%s, %s, %s, %s)'

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(queryFindUser, (username,))
            result = cursor.fetchone()
            if not result:
                return 'Usuario no encontrado', 401
            user_id = result['usuario_id']

            cursor.execute(queryFindAlbum, (album, user_id))
            result = cursor.fetchone()
            if not result:
                return 'Álbum no encontrado', 401
            album_id = result['album_id']

            local_foto = f'./uploads/{album}_{nombre_foto}.jpg'

            s3_foto = f'{album}/{nombre_foto}.jpg'

            image = base64.b64decode(foto_base64)

            with open(local_foto, 'wb') as file:
                file.write(image)

            s3_client.upload_file(local_foto, os.getenv('S3_BUCKET'), s3_foto)

            url_foto = f'https://{os.getenv("S3_BUCKET")}.s3.amazonaws.com/{s3_foto}'
            cursor.execute(queryInsertPhoto, (nombre_foto, url_foto, album_id, user_id))

            conn.commit()
    except Exception as e:
        print(e)
        return 'Error al crear foto', 500
    finally:
        conn.close()

    return 'Foto creada', 200

@app.route('/api/fotos/usuario/<usuario>', methods=['GET'])
def photos_by_user(usuario):
    query = "SELECT f.nombre, f.url, a.nombre as album FROM fotos f JOIN albumes a ON f.album_id = a.album_id JOIN usuarios u ON f.usuario_id = u.usuario_id WHERE u.usuario = %s"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (usuario,))
            result = cursor.fetchall()
            if not result:
                return 'Usuario no encontrado', 401
    except Exception as e:
        print(e)
        return 'Error al obtener fotos', 500
    finally:
        conn.close()

    return jsonify(result), 200

@app.route('/api/fotos/album/<album>', methods=['GET'])
def photos_by_album(album):
    query = "SELECT f.nombre, f.url, u.usuario FROM fotos f JOIN albumes a ON f.album_id = a.album_id JOIN usuarios u ON f.usuario_id = u.usuario_id WHERE a.nombre = %s"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (album,))
            result = cursor.fetchall()
            if not result:
                return 'Álbum no encontrado', 401
    except Exception as e:
        print(e)
        return 'Error al obtener fotos', 500
    finally:
        conn.close()

    return jsonify(result), 200

@app.route('/api/albumes', methods=['POST'])
def create_album():
    data = request.json
    nombre_album, username, desc = data['nombre_album'], data['username'], data['desc']

    queryFindUser = 'SELECT usuario_id FROM usuarios WHERE usuario = %s'

    queryInsertAlbum = 'INSERT INTO albumes (nombre, descripcion, usuario_id) VALUES (%s, %s, %s)'

    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(queryFindUser, (username,))
            result = cursor.fetchone()
            if not result:
                return 'Usuario no encontrado', 401
            user_id = result['usuario_id']

            cursor.execute(queryInsertAlbum, (nombre_album, desc, user_id))
            conn.commit()
    except Exception as e:
        print(e)
        return 'Error al crear álbum', 500
    finally:
        conn.close()

    return 'Álbum creado', 200

@app.route('/api/albumes/usuario/<usuario>', methods=['GET'])
def albums_by_user(usuario):
    query = "SELECT nombre, descripcion FROM albumes a JOIN usuarios u ON a.usuario_id = u.usuario_id WHERE u.usuario = %s"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (usuario,))
            result = cursor.fetchall()
            if not result:
                return 'Usuario no encontrado', 401
    except Exception as e:
        print(e)
        return 'Error al obtener álbumes', 500
    finally:
        conn.close()

    return jsonify(result), 200

@app.route('/api/albumes/album/<album>', methods=['PUT'])
def update_album(album):
    data = request.json
    nuevo_nombre, desc = data['nuevo_nombre'], data['desc']

    query = "UPDATE albumes SET nombre = %s, descripcion = %s WHERE nombre = %s"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (nuevo_nombre, desc, album))
            conn.commit()
    except Exception as e:
        print(e)
        return 'Error al actualizar álbum', 500
    finally:
        conn.close()

    return 'Álbum actualizado', 200

@app.route('/api/albumes/album/<album>', methods=['DELETE'])
def delete_album(album):
    query = "DELETE FROM albumes WHERE nombre = %s"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (album,))
            conn.commit()
    except Exception as e:
        print(e)
        return 'Error al eliminar álbum', 500
    finally:
        conn.close()

    return 'Álbum eliminado', 200

@app.route('/api/usuarios/fotoPerfil', methods=['PUT'])
def update_photo_profile():
    data = request.json
    usuario, photo_url = data['usuario'], data['photo_url']

    query = "UPDATE usuarios SET foto_perfil_url = %s WHERE usuario = %s"
    
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (photo_url, usuario))
            conn.commit()
    except Exception as e:
        print(e)
        return 'Error al actualizar foto de perfil', 500
    finally:
        conn.close()

    return 'Foto de perfil actualizada', 200

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
