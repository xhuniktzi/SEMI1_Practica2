import { AfterViewInit, Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { ApiService } from '../api.service';


@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss']
})
export class DashboardComponent implements OnInit, AfterViewInit {
  username: string = '';

  nickname: string = '';
  nombre: string = '';
  rutaFotoPerfil: string = '';

  constructor(private route: ActivatedRoute, private api: ApiService) { }

  ngOnInit(): void {
    this.route.paramMap.subscribe(params => {

      this.username = params.get('username')!;
    });
  }

  ngAfterViewInit(): void {
    this.api.getProfile(this.username).subscribe({
      next: (response) => {
       if ('nickname' in response) {
          this.nickname = response.nickname;
        }

        if ('nombre' in response) {
          this.nombre = response.nombre;
        }

        if ('rutaFotoPerfil' in response) {
          this.rutaFotoPerfil = response.rutaFotoPerfil;
        }

        if ('message' in response) {
          alert(response.message);
        }
      },
      error: (error) => {
        alert(error.error.message);
      }
    });

  }
}
