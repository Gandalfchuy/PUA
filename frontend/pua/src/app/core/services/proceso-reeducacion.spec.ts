import { TestBed } from '@angular/core/testing';

import { ProcesoReeducacion } from './proceso-reeducacion';

describe('ProcesoReeducacion', () => {
  let service: ProcesoReeducacion;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ProcesoReeducacion);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
