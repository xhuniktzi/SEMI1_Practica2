import base64
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import pymysql.cursors
import hashlib
import boto3
import dotenv
import botocore


# Configuración de la conexión a la base de datos
def get_db_connection():
    return pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_SCHEMA"),
        cursorclass=pymysql.cursors.DictCursor,
    )


# Función para generar MD5
def generate_md5(data):
    return hashlib.md5(data.encode()).hexdigest()


app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
dotenv.load_dotenv()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("S3_PUBLIC_ACCESS"),
    aws_secret_access_key=os.getenv("S3_SECRET_ACCESS"),
    region_name="us-east-1",
)

rekognition_client = boto3.client(
    "rekognition",
    aws_access_key_id=os.getenv("REKOGNITION_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("REKOGNITION_SECRET_ACCESS"),
    region_name="us-east-1",
)

translate = boto3.client(
    "translate",
    aws_access_key_id=os.getenv("TRANSLATE_ACCESS_KEY"),
    aws_secret_access_key=os.getenv("TRANSLATE_SECRET_ACCESS"),
    region_name="us-east-1",
)


@app.route("/usuarios/registro", methods=["POST"])
def registro_usuario():
    data = request.json
    nickname = data["usuario"]
    nombre = data["nombre_completo"]
    password = generate_md5(data["password"])
    photo_base64 = data["photo_base64"]

    # Convierte la imagen base64 a bytes
    photo_data = base64.b64decode(photo_base64)
    photo_path = f"Fotos_perfil/{nickname}.jpg"

    # Subir la foto a S3
    s3_client.put_object(Bucket=os.getenv("S3_BUCKET"), Key=photo_path, Body=photo_data)

    # Guardar en la base de datos
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO Usuarios (nickname, nombre, password, rutaFotoPerfil) VALUES (%s, %s, %s, %s)",
            (nickname, nombre, password, photo_path),
        )
        connection.commit()

    return jsonify({"message": "Usuario registrado con éxito"}), 201


@app.route("/usuarios/login", methods=["POST"])
def login_usuario():
    data = request.json
    nickname = data["usuario"]
    password = data.get("password")
    photo_base64 = data.get("photo_base64")
    connection = get_db_connection()

    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Usuarios WHERE nickname = %s", (nickname,))
        user = cursor.fetchone()

    if not user:
        return jsonify({"message": "Usuario no encontrado"}), 404

    # Autenticación con contraseña
    if password:
        if generate_md5(password) == user["password"]:
            return jsonify({"message": "Login exitoso"}), 200
        else:
            return jsonify({"message": "Contraseña incorrecta"}), 401

    # Autenticación con foto
    if photo_base64:
        # Convierte la imagen base64 a bytes y la guarda temporalmente
        photo_data = base64.b64decode(photo_base64)
        temp_photo_path = f"temp_{nickname}.jpg"
        with open(temp_photo_path, "wb") as file:
            file.write(photo_data)

        # Obtener la imagen del usuario desde S3
        bucket_name = os.getenv("S3_BUCKET")
        object_key = user[
            "rutaFotoPerfil"
        ]  # Asumiendo que rutaFotoPerfil contiene la clave del objeto en S3
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        user_image_bytes = response["Body"].read()

        try:
            # Realiza la comparación de rostros con AWS Rekognition
            response = rekognition_client.compare_faces(
                SourceImage={"Bytes": user_image_bytes},
                TargetImage={"Bytes": open(temp_photo_path, "rb").read()},
            )
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "InvalidParameterException":
                # Elimina la foto temporal
                os.remove(temp_photo_path)
                return (
                    jsonify(
                        {"message": "La imagen enviada no contiene una cara válida"}
                    ),
                    400,
                )
            else:
                raise e

        # Elimina la foto temporal
        os.remove(temp_photo_path)

        # Verifica si los rostros coinciden
        if response["FaceMatches"]:
            return jsonify({"message": "Login exitoso con foto"}), 200
        else:
            return jsonify({"message": "Login fallido con foto"}), 401

    return (
        jsonify(
            {"message": "Debe proporcionar una contraseña o una foto para el login"}
        ),
        400,
    )


@app.route("/usuarios/perfil/<username>", methods=["GET"])
def obtener_perfil(username):
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Usuarios WHERE nickname = %s", (username,))
        user = cursor.fetchone()

    if user:
        del user["password"]  # No devolver la contraseña
        del user["id"]  # No devolver el ID

        # Obtener la foto del usuario desde S3
        bucket_name = os.getenv("S3_BUCKET")
        object_key = user["rutaFotoPerfil"]
        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        user_image_bytes = response["Body"].read()

        # Obtener la descripción de la foto con AWS Rekognition
        response = rekognition_client.detect_faces(
            Image={"Bytes": user_image_bytes}, Attributes=["ALL"]
        )

        if response["FaceDetails"]:
            face_details = response["FaceDetails"][0]
            age_range = face_details["AgeRange"]
            gender = face_details["Gender"]["Value"]
            emotions = [
                emotion["Type"]
                for emotion in face_details["Emotions"]
                if emotion["Confidence"] > 50
            ]
            accessories = face_details.get("Accessories", [])
            accessories = [
                accessor for accessor in accessories if accessor["Confidence"] > 50
            ]

            description = f"Persona {gender} de entre {age_range['Low']} y {age_range['High']} años de edad"
            if emotions:
                description += f" con expresiones de {', '.join(emotions)}"
            if accessories:
                description += (
                    f" usando {', '.join(accessor['Type'] for accessor in accessories)}"
                )

            # Agregar la descripción al diccionario del usuario
            user["descripcion"] = description

        return jsonify(user), 200
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404


@app.route("/fotos", methods=["POST"])
def subir_foto():
    data = request.json
    username = data["username"]
    titulo = data["nombre"]
    descripcion = data["descripcion"]
    photo_base64 = data["photo_base64"]

    # Subir la foto a S3
    photo_data = base64.b64decode(photo_base64)
    photo_path = f"Fotos_publicadas/{username}/{titulo}.jpg"
    s3_client.put_object(Bucket=os.getenv("S3_BUCKET"), Key=photo_path, Body=photo_data)

    # Obtener etiquetas de AWS Rekognition
    response = rekognition_client.detect_labels(
        Image={"S3Object": {"Bucket": os.getenv("S3_BUCKET"), "Name": photo_path}}
    )
    etiquetas = [label["Name"] for label in response["Labels"]]

    # Guardar foto y etiquetas en la base de datos
    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            "INSERT INTO Fotos (titulo, descripcion, rutaFoto, usuarioId) VALUES (%s,%s, %s, (SELECT id FROM Usuarios WHERE nickname = %s))",
            (titulo, descripcion, photo_path, username),
        )
        foto_id = cursor.lastrowid

        for etiqueta in etiquetas:
            cursor.execute(
                "INSERT INTO Etiquetas (etiqueta) VALUES (%s) ON DUPLICATE KEY UPDATE id=LAST_INSERT_ID(id)",
                (etiqueta,),
            )
            etiqueta_id = cursor.lastrowid
            cursor.execute(
                "INSERT INTO FotoEtiquetas (fotoId, etiquetaId) VALUES (%s, %s)",
                (foto_id, etiqueta_id),
            )

        connection.commit()

    return jsonify({"message": "Foto subida con éxito"}), 201


@app.route("/usuarios/perfil/<username>", methods=["PUT"])
def actualizar_perfil(username):
    data = request.json
    password = data["password"]

    # Validación de password siempre presente
    if not password:
        return jsonify({"message": "La contraseña es requerida"}), 400

    # Extraer los campos, si no están presentes serán None
    new_username = data.get("usuario")
    nombre_completo = data.get("nombre_completo")
    photo_base64 = data.get("photo_base64")

    connection = get_db_connection()
    with connection.cursor() as cursor:
        cursor.execute(
            "SELECT password, nickname, nombre, rutaFotoPerfil FROM Usuarios WHERE nickname = %s",
            (username,),
        )
        user = cursor.fetchone()

        if not user:
            return jsonify({"message": "Usuario no encontrado"}), 404

        if generate_md5(password) != user["password"]:
            return jsonify({"message": "Contraseña incorrecta"}), 401

        # Actualizar la foto si está presente
        if photo_base64:
            photo_data = base64.b64decode(photo_base64)
            photo_path = (
                f"Fotos_perfil/{new_username if new_username else user['nickname']}.jpg"
            )
            s3_client.put_object(
                Bucket=os.getenv("S3_BUCKET"), Key=photo_path, Body=photo_data
            )
        else:
            photo_path = user[
                "rutaFotoPerfil"
            ]  # Mantener la ruta existente si no se actualiza la foto

        # Definir nuevos valores o mantener los actuales si los campos están vacíos
        new_username = new_username if new_username else user["nickname"]
        nombre_completo = nombre_completo if nombre_completo else user["nombre"]

        # Actualización en la base de datos
        cursor.execute(
            "UPDATE Usuarios SET nickname = %s, nombre = %s, rutaFotoPerfil = %s WHERE nickname = %s",
            (new_username, nombre_completo, photo_path, username),
        )
        connection.commit()
        return jsonify({"message": "Perfil actualizado"}), 200


@app.route("/fotos/<username>", methods=["GET"])
def obtener_fotos_usuario(username):
    connection = get_db_connection()
    fotos = []
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT f.id, f.titulo, f.descripcion, f.rutaFoto, u.nickname
            FROM Fotos f
            JOIN Usuarios u ON f.usuarioId = u.id
            WHERE u.nickname = %s
        """,
            (username,),
        )
        fotos = cursor.fetchall()

        for foto in fotos:

            cursor.execute(
                """
                SELECT e.etiqueta
                FROM FotoEtiquetas fe
                JOIN Etiquetas e ON fe.etiquetaId = e.id
                WHERE fe.fotoId = %s
            """,
                (foto["id"],),
            )
            etiquetas = cursor.fetchall()
            foto["etiquetas"] = [etiqueta["etiqueta"] for etiqueta in etiquetas]
            del foto["id"]
            del foto["nickname"]

            description = foto["descripcion"]

            description_en = translate.translate_text(
                Text=description, SourceLanguageCode="es", TargetLanguageCode="en"
            )["TranslatedText"]

            description_fr = translate.translate_text(
                Text=description, SourceLanguageCode="es", TargetLanguageCode="fr"
            )["TranslatedText"]

            description_zh = translate.translate_text(
                Text=description, SourceLanguageCode="es", TargetLanguageCode="zh"
            )["TranslatedText"]

            foto["descripcion"] = (
                "Español: "
                + description
                + " | Inglés: "
                + description_en
                + " | Francés: "
                + description_fr
                + " | Chino: "
                + description_zh
            )
    return jsonify(fotos), 200


@app.route("/extract_text", methods=["POST"])
def extract_text_from_image():
    data = request.json
    image_base64 = data.get("image_base64")

    if not image_base64:
        return jsonify({"message": "No se proporcionó una imagen"}), 400

    # Decodificar la imagen base64
    image_data = base64.b64decode(image_base64)

    # Detectar texto en la imagen con AWS Rekognition
    response = rekognition_client.detect_text(Image={"Bytes": image_data})

    # Extraer el texto detectado
    detected_text = []
    for text_detection in response["TextDetections"]:
        detected_text.append(text_detection["DetectedText"])

    return jsonify({"detected_text": detected_text})


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
