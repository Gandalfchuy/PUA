import { TestBed } from '@angular/core/testing';

import { Sesiones } from './sesiones';

describe('Sesiones', () => {
  let service: Sesiones;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(Sesiones);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
