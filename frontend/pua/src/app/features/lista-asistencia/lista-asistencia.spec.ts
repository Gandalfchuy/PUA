import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ListaAsistencia } from './lista-asistencia';

describe('ListaAsistencia', () => {
  let component: ListaAsistencia;
  let fixture: ComponentFixture<ListaAsistencia>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ListaAsistencia],
    }).compileComponents();

    fixture = TestBed.createComponent(ListaAsistencia);
    component = fixture.componentInstance;
    await fixture.whenStable();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
