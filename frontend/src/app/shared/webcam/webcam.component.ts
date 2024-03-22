import { Component, ElementRef, EventEmitter, Input, Output, ViewChild, OnDestroy, AfterViewInit } from '@angular/core';

@Component({
  selector: 'app-webcam',
  templateUrl: './webcam.component.html',
  styleUrls: ['./webcam.component.scss']
})
export class WebcamComponent implements OnDestroy, AfterViewInit {
  @Input() buttonVisible = true;
  @Output() imageCaptured: EventEmitter<string> = new EventEmitter<string>();
  @ViewChild('videoElement') videoElement!: ElementRef;
  video!: HTMLVideoElement;
  stream?: MediaStream; // Declarar una propiedad para almacenar el stream de la cámara

  ngAfterViewInit() {
    this.video = this.videoElement.nativeElement;
    this.initCamera();
  }

  initCamera() {
    if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
      navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
          this.stream = stream; // Almacenar el stream de la cámara
          this.video.srcObject = stream;
          this.video.play();
        })
        .catch(error => {
          console.error("Error accessing the camera", error);
        });
    } else {
      alert('Su navegador no soporta acceso a la cámara');
    }
  }

  capture() {
    const canvas = document.createElement('canvas');
    canvas.width = this.video.videoWidth;
    canvas.height = this.video.videoHeight;
    const ctx = canvas.getContext('2d')!;
    ctx.drawImage(this.video, 0, 0, canvas.width, canvas.height);
    const imageDataUrl = canvas.toDataURL('image/png');
    const parsedDataUrl = imageDataUrl.split('data:image/png;base64,')[1];
    this.imageCaptured.emit(parsedDataUrl); // Emite el valor al componente padre
  }

  ngOnDestroy() {
    if (this.stream) {
      this.stream.getTracks().forEach(track => track.stop()); // Detener todas las pistas del stream de la cámara
    }
  }
}