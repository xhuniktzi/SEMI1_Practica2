import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ExtractTextComponent } from './extract-text.component';

describe('ExtractTextComponent', () => {
  let component: ExtractTextComponent;
  let fixture: ComponentFixture<ExtractTextComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ExtractTextComponent]
    });
    fixture = TestBed.createComponent(ExtractTextComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
