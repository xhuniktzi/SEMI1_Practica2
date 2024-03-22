import { Injectable } from '@angular/core';
import { IRegistroRequest } from './models/IRegistroRequest';
import { HttpClient } from '@angular/common/http';
import { IMessageResponse } from './models/IMessageResponse';
import { Observable } from 'rxjs';
import { ILoginRequest } from './models/ILoginRequest';
import { IGetProfileResponse } from './models/IGetProfileResponse';
import { IUploadPhotoRequest } from './models/IUploadPhotoRequest';
import { IUpdateProfileRequest } from './models/IUpdateProfileRequest';
import { IGetPhotosResponse } from './models/IGetPhotosResponse';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  baseUrl = 'http://localhost:5000';
  constructor(private http: HttpClient) { }

  register(request: IRegistroRequest): Observable<IMessageResponse> {
    return this.http.post<IMessageResponse>(`${this.baseUrl}/usuarios/registro`, request)
  }

  login(request: ILoginRequest): Observable<IMessageResponse> {
    return this.http.post<IMessageResponse>(`${this.baseUrl}/usuarios/login`, request)
  }

  getProfile(username: string): Observable<IMessageResponse | IGetProfileResponse>  {
    return this.http.get<IMessageResponse | IGetProfileResponse>(`${this.baseUrl}/usuarios/perfil/${username}`)
  }

  uploadPhoto(request: IUploadPhotoRequest): Observable<IMessageResponse> {
    return this.http.post<IMessageResponse>(`${this.baseUrl}/fotos`, request)
  }

  updateProfile(request: IUpdateProfileRequest, username: string): Observable<IMessageResponse> {
    return this.http.put<IMessageResponse>(`${this.baseUrl}/usuarios/perfil/${username}`, request)
  }

  getPhotos(username: string): Observable<Array<IGetPhotosResponse>> {
    return this.http.get<Array<IGetPhotosResponse>>(`${this.baseUrl}/fotos/${username}`)
  }
}
